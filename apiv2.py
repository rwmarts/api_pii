import json
import flask
import httplib2
from apiclient import discovery
from oauth2client import client
from flask_restful import Resource, Api, abort
from mysqlfnc import connect, run_query
from collections import OrderedDict


application = Flask(__name__)
api = Api(application)

def bit_to_bool(value):
    return value > 0

class PiiApi(Resource):
    def execute_query(self, query):
        con = connect('localhost', 3306, 'yoda', 'dagobah', 'pii_db')
        cursor = run_query(con, query)
        con.commit()
        con.close()
        return cursor

    def map_query(self, query, mapping, allow_empty_set=True):
        result = []
        cursor = self.execute_query(query)
        rows = cursor.fetchall()
        if len(rows) == 0 and not allow_empty_set:
            abort(404, message='No resource found')
        for row in rows:
            if len(row) != len(mapping):
                print "Field mismatch!"
                exit()
            rowdict = OrderedDict()
            for index in range(len(row)):
                rowdict[mapping[index]] = row[index]
            result.append(rowdict)
        return result


    def send_response(self, payload='', response_code=200):
        response = {
            'response_code': response_code,
            'errors': [],
            'payload': payload
        }
        return jsonify(response)


    def id_exists(self, table, field, value):
        query = "select count(*) from {} where {} = '{}'".format(table, field, value)
        c = self.execute_query(query)
        rows = c.fetchall()
        return len(rows) == 1

    def get(self):
        return 'This is the API for the PII Tool'


class VariableDomainList(PiiApi):
    def get(self, active):
        if active not in [0, 1]:
            active = 1 # Default
        mapping = ['value', 'label']
        query = 'select client_domains_id, client_domain from client_domains where active = {}'.format(active)
        result = self.map_query(query, mapping)
        return self.send_response(result)

class DomainList(VariableDomainList):
    def get(self):
        return super(DomainList, self).get(1)

class Domain(PiiApi):
    def get(self, domain_id):
        mapping = ['value', 'label', 'selected']
        query = 'select client_domains_id, client_domain, active from client_domains where client_domains_id = {}'.format(domain_id)
        result = self.map_query(query, mapping)
        return self.send_response(result)

class VariableProviderList(PiiApi):
    def get(self, active):
        if active not in [0, 1]:
            active = 1 # Default
        mapping = ['value', 'label']
        query = 'select providers_id, provider from providers where active = {}'.format(active)
        result = self.map_query(query, mapping)
        return self.send_response(result)

class ProviderList(VariableProviderList):
    def get(self):
        return super(ProviderList, self).get(1)

class Provider(PiiApi):
    def get(self, provider_id):
        mapping = ['value', 'label', 'selected']
        query = 'select providers_id, provider, active from providers where providers_id = {}'.format(provider_id)
        result = self.map_query(query, mapping)
        return self.send_response(result)


class VariableFrequencyList(PiiApi):
    def get(self, active):
        if active not in [0, 1]:
            active = 1 # Default
        mapping = ['value', 'label']
        query = 'select frequencies_id, frequency from frequencies where active ={}'.format(active)
        result = self.map_query(query, mapping)
        return self.send_response(result)


class FrequencyList(VariableFrequencyList):
    def get(self):
        return super(FrequencyList, self).get(1)


class Frequency(PiiApi):
    def get(self, frequency_id):
        mapping = ['value', 'label', 'selected']
        query = 'select frequencies_id, frequency, active from frequencies where frequencies_id = {}'.format(frequency_id)
        result = self.map_query(query, mapping)
        return self.send_response(result)


class DomainMailList(PiiApi):
    def get(self, domain_id):
        mapping = ['value', 'label', 'selected']
        query = 'select user_id, email, active from users where user_id in (select user_id from users_client_domains where client_domains_id = {})'.format(domain_id)
        result = self.map_query(query, mapping)
        return self.send_response(result)


class ProviderClientList(PiiApi):
    def get(self, provider_id):
        mapping = ['value', 'label', 'selected']
        query = 'select client_domains_id, client_domain, active from client_domains where user_id in (select client_domains_id from provider_clients where provider_id = {})'.format(provider_id)
        result = self.map_query(query, mapping)
        return self.send_response(result)


class ProviderMetricsList(PiiApi):
    def get(self, provider_id):
        mapping = ['value', 'label']
        query = 'select metrics_id, metric from metrics where metric_id in (select metric_id from provider_metrics where provider_id = {})'.format(provider_id)
        result = self.map_query(query, mapping)
        return self.send_response(result)


class Schedules(PiiApi):
    def get(self):
        """
        Needed here are all schedules (by nmpi_user_id?), then by association
        - Frequencies,
        - Emails

        Buildup should be like:
        get all schedules(id, providerid, frequencyid)
        """
        mapping = ['scheduleId', 'domainId', 'providerId', 'frequencyId']
        sched_query = 'select schedules_id, client_domain_id, providers_id, frequencies_id from schedules'
        schedules = self.map_query(sched_query, mapping)
        # Now add associated emails
        mail_mapping = ['value', 'label', 'selected']
        for schedule in schedules:
            user_query = 'select users_id, email, active from users where user_types_id = 2 and users_id in (select users_id from users_schedules where schedules_id = {})'.format(schedule['scheduleId'])
            users = self.map_query(user_query, mail_mapping)
            for user in users:
                user['selected'] = bit_to_bool(user['selected'])
            schedule['emails'] = users
        return self.send_response(schedules)

class ScheduleEdit(PiiApi):
    def get(self):
        return "Error: Incorrect use"

    def post(self):
        data = request.get_json(force=True)
        if self.validate_fields(data):
            if 'scheduleId' in data:
                response = self.update_schedule(data)
            else:
                response = self.create_schedule(data)
        else:
            response = {"success": False}
        return self.send_response(response)

    def create_schedule(self, fields):
        query = "insert into schedules(providers_id, frequencies_id, client_domain_id, expires, hash, active) values ({}, {}, {}, now(), '', 1)".format(fields['providerId'], fields['frequencyId'], fields['domainId'])
        c = self.execute_query(query)
        self.add_emails(c.lastrowid, fields['emailIds'])
        response = {"success": True}
        return response

    def update_schedule(self, fields):
        query = "update schedules set providers_id = {}, frequencies_id = {}, client_domain_id ={} where schedules_id = []".format(fields['providerId'], fields['frequencyId'], fields['domainId'], fields['scheduleId'])
        self.remove_emails(fields['scheduleId'])
        self.add_emails(fields['scheduleId'], fields['emailIds'])
        response = {"success": True}
        return response


    def validate_fields(self, fields):
        """
        The following fields exist for the schedule call:
        scheduleId: int (optional)
        providerId: int
        frequencyId: int
        domainId: int
        emailIds: list of ints
        A field is valid when (a) the type check succeeds (b) it is an existing entry
        TODO: Clean up
        """
        # Treat emailIds later, this is a list
        valid = True
        if 'scheduleId' in fields:
            valid = type(fields['scheduleId']) is int
            if valid:
                valid = valid and self.id_exists('schedules', 'schedules_id', fields['scheduleId'])
        valid = valid and type(fields['providerId']) is int
        if valid:
            valid = valid and self.id_exists('providers', 'providers_id', fields['providerId'])
        valid = valid and type(fields['frequencyId']) is int
        if valid:
            valid = valid and self.id_exists('frequencies', 'frequencies_id', fields['frequencyId'])
        valid = valid and type(fields['domainId']) is int
        if valid:
            valid = valid and self.id_exists('client_domains', 'client_domains_id', fields['domainId'])

        # Check Email Ids
        for id in fields['emailIds']:
            valid = valid and id is int
            if valid:
                valid = valid and self.id_exists('users', 'users_id', id)

        return valid


    def add_emails(self, scheduleId, emails):
        for email in emails:
            query = "insert into user_schedules(schedules_id, users_id) values ({}, {})".format(
                scheduleId, email)
            self.execute_query(query)



    def remove_emails(self, scheduleId):
        query = "delete from user_schedules where schedules_id = {}".format(scheduleId)
        self.execute_query(query)


class ScheduleDelete(PiiApi):

    def get(self, scheduleId):
        # Start off naive
        # TODO: scrub associative tables
        query = "delete from schedules where schedules_id = {}".format(scheduleId)
        self.execute_query(query)
        response = {"success": True}
        return response


api.add_resource(PiiApi, '/api')
api.add_resource(DomainList, '/domains')
api.add_resource(VariableDomainList, '/domains/<int:active>')
api.add_resource(Domain, '/domain/<int:domain_id>')
api.add_resource(ProviderList, '/providers')
api.add_resource(Provider, '/provider/<int:provider_id>')
api.add_resource(FrequencyList, '/frequencies')
api.add_resource(Frequency, '/frequency/<int:frequency_id>')
api.add_resource(DomainMailList, '/emails/<int:domain_id>')
api.add_resource(ProviderClientList, '/provider-clients/<int:provider_id>')
api.add_resource(ProviderMetricsList, '/provider-metrics/<int:provider_id>')
api.add_resource(Schedules, '/schedules')
api.add_resource(ScheduleEdit, '/schedule')
api.add_resource(ScheduleDelete, '/schedule/delete/<int:schedule_id>')


# Get a starting point for our tests
# Flask routes

def authorize(user):
    authenticated = False
    emails = user['emails']
    for email in emails:
        sql = 'select users_id, user_types_id from users where email = "{}"'
        c = execute_query(sql)
        rows = c.fetchall()
        if len(rows) == 1:
            row = rows[0]
            flask.session['userid'] = row[0]
            flask.session['usertype'] = row[1]
            flask.session['email'] = email
            authenticated = True
            break;
    if not authenticated:
        flask.session.clear()
    return authenticated



def execute_query(self, query):
    con = connect('localhost', 3306, 'yoda', 'dagobah', 'pii_db')
    cursor = run_query(con, query)
    con.commit()
    con.close()
    return cursor


@application.route('/login')
def login():
  if 'credentials' not in flask.session:
    return flask.redirect(flask.url_for('oauth2callback'))
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  if credentials.access_token_expired:
    return flask.redirect(flask.url_for('oauth2callback'))
  else:
    http_auth = credentials.authorize(httplib2.Http())
    plus = discovery.build('plus', 'v1', http_auth)
    people = plus.people()
    me = people.get(userId='me').execute()
    authenticated = authorize(me)
    if authenticated:
        return flask.redirect(flask.url_for('index'))
    return flask.redirect(flask.url_for('forbidden'))


@application.route('/oauth2callback')
def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'client_secrets.json',
      scope='https://www.googleapis.com/auth/plus.me',
      redirect_uri=flask.url_for('oauth2callback', _external=True),
      )
  if 'code' not in flask.request.args:
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    flask.session['credentials'] = credentials.to_json()
    return flask.redirect(flask.url_for('index'))

@application.route("/tests")
def testpage():
    return render_template('page.html')


if __name__ == '__main__':
    application.run(debug=True)
