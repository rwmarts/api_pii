from flask import Flask, jsonify
from mysqlfnc import connect, run_query


app = Flask(__name__)

def fetch_result(query):
    con = connect('localhost', 3306, 'yoda', 'dagobah', 'pii_db')
    cursor = run_query(con, query)
    con.close()
    return cursor

def generate_response(cursor, mapping):
    result = []
    rows = cursor.fetchall()
    for row in rows:
        if len(row) != len(mapping):
            print "Field mismatch!"
            exit()
        rowdict = {}
        for index in range(len(row)):
            rowdict[mapping[index]] = row[index]
        result.append(rowdict)
    return result

def process_query(query, mapping):
    cursor = fetch_result(query)
    result = generate_response(cursor, mapping)
    return result

@app.route("/")
def index():
    return "Pii Api Endpoint"


@app.route("/domains")
def domains():
    # Database queries for domains
    # Possible response:
    response = [
        {
            "value": "d1",
            "label": "bathstore.com",
            "selected": False
        },
        {
            "value": "d2",
            "label": "superdrug.com",
            "selected": False
        },
        {
            "value": "d3",
            "label": "papajohns.com",
            "selected": False
        }
    ]
    return send_response(response)

@app.route("/providers")
def providers():
    # Database queries for providers
    # Possible response:
    response = [
        {
            "value": "p1",
            "label": "Facebook",
            "selected": False
        },
        {
            "value": "p2",
            "label": "Google Adwords",
            "selected": False
        }
    ]
    return send_response(response)

@app.route("/frequencies")
def frequencies():
    # Database queries for frequencies
    # Possible response:
    response = [
        {
            "value": "f1",
            "label": "Once",
            "selected": False
        },
        {
            "value": "f3",
            "label": "Weekly",
            "selected": False
        },
        {
            "value": "f4",
            "label": "Monthly",
            "selected": False
        }
    ]
    return send_response(response)


@app.route("/schedules")
def schedules():
    # Database queries for schedules
    # Possible response:
    response = [
        {
            "scheduleId": "s1",
            "scheduleDomains": [
                {
                    "value": "d1",
                    "label": "bathstore.com",
                    "selected": True
                },
                {
                    "value": "d2",
                    "label": "superdrug.com",
                    "selected": False
                },
                {
                    "value": "d3",
                    "label": "papajohns.com",
                    "selected": False
                }
            ],
            "scheduleProviders": [
                {
                    "value": "p1",
                    "label": "Facebook",
                    "selected": True
                },
                {
                    "value": "p2",
                    "label": "Google Adwords",
                    "selected": False
                }
            ],
            "scheduleFrequencies": [
                {
                    "value": "f1",
                    "label": "Once",
                    "selected": False
                },
                {
                    "value": "f3",
                    "label": "Weekly",
                    "selected": False
                },
                {
                    "value": "f4",
                    "label": "Monthly",
                    "selected": True
                }
            ],
            "scheduleEmails": [
                {
                    "value": "e1",
                    "label": "john@bathstore.com",
                    "selected": True
                },
                {
                    "value": "e2",
                    "label": "jack@bathstore.com",
                    "selected": False
                },
                {
                    "value": "e3",
                    "label": "silvia@bathstore.com",
                    "selected": False
                }
            ],
            "updated": False
        },
        {
            "scheduleId": "s2",
            "scheduleDomains": [
                {
                    "value": "d1",
                    "label": "bathstore.com",
                    "selected": False
                },
                {
                    "value": "d2",
                    "label": "superdrug.com",
                    "selected": True
                },
                {
                    "value": "d3",
                    "label": "papajohns.com",
                    "selected": False
                }
            ],
            "scheduleProviders": [
                {
                    "value": "p1",
                    "label": "Facebook",
                    "selected": False
                },
                {
                    "value": "p2",
                    "label": "Google Adwords",
                    "selected": True
                }
            ],
            "scheduleFrequencies": [
                {
                    "value": "f1",
                    "label": "Once",
                    "selected": False
                },
                {
                    "value": "f3",
                    "label": "Weekly",
                    "selected": True
                },
                {
                    "value": "f4",
                    "label": "Monthly",
                    "selected": False
                }
            ],
            "scheduleEmails": [
                {
                    "value": "e4",
                    "label": "mario@superdrug.com",
                    "selected": True
                },
                {
                    "value": "e5",
                    "label": "elena@superdrug.com",
                    "selected": False
                },
                {
                    "value": "e6",
                    "label": "masha@superdrug.com",
                    "selected": False
                }
            ],
            "updated": False
        }
    ]
    return send_response(response)





def send_response(payload=''):
    response = {
        'response_code': 200,
        'errors': [],
        'payload': payload
    }
    return jsonify(response)



if __name__ == "__main__":
    app.run()
