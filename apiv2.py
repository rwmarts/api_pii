from flask import Flask, request, jsonify
from flask_restful import Resource, Api, abort
from mysqlfnc import connect, run_query
from collections import OrderedDict


application = Flask(__name__)
api = Api(application)

def bit_to_bool(value):
    return value > 0

class PiiApi(Resource):
    def fetch_result(self, query):
        con = connect('localhost', 3306, 'yoda', 'dagobah', 'pii_db')
        cursor = run_query(con, query)
        con.close()
        return cursor

    def map_query(self, query, mapping, allow_empty_set=True):
        result = []
        cursor = self.fetch_result(query)
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
            print user_query
            users = self.map_query(user_query, mail_mapping)
            schedule['emails'] = users
            for user in users:
                user['selected'] = bit_to_bool(user['selected'])
        return self.send_response(schedules)



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

if __name__ == '__main__':
    application.run(debug=True)
