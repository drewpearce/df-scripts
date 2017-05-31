import json
import requests
import random
from pprint import pprint

def build_payload(this_counter, record_count):
    this_payload = {}
    this_payload['resource'] = []

    while this_counter <= record_count:
        record = {}
        record['name'] = 'Record #{}'.format(this_counter)
        record['complete'] = random.choice([True, False])
        this_payload['resource'].append(record)
        this_counter += 1
    this_payload = json.dumps(this_payload)


def build_url(base_url):
    if base_url[-1:] == '/':
        base_url = base_url[:-1]
    url = '{}/api/v2/{}/_table/{}'.format(base_url, service, table)
    return url


def build_auth():
    auth = ('{}'.format(admin_user), '{}'.format(admin_password))
    return auth


#base_url = input('What is the base_url? (ex: http://localhost.com:8080) ')
base_url = 'http://df.local:8080'
#service = input('What service do you want to use? ')
service = 'upserttest'
#table = input('What table do you want to use? ')
table = 'todo'
#admin_user = input('What is the admin user\'s email? ')
admin_user = 'drew@dreamfactory.com'
#admin_password = input('What is the admin user\'s password? ')
admin_password = 'password'
record_count = input('How many records would you like to make? ')
record_count = int(record_count)

payload = build_payload(1, record_count)
url = build_url(base_url)
authorization = build_auth()

print(url)
pprint(authorization)
pprint(payload)

#post_records = requests.post(service_url, auth=call_auth, data=payload)

#pprint(post_records.status_code)

#if post_records.status_code == requests.codes.ok:
#    result = json.loads(post_records.text)
#    pprint(result)
