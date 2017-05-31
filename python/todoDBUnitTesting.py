import requests
import json
import random
from string import ascii_lowercase
import sys
import time
from pprint import pprint

def generate_rands():
    response = {}
    response['name'] = ''.join((random.choice(ascii_lowercase)) for x in range(10))
    response['password'] = ''.join((random.choice(ascii_lowercase)) for x in range(20))
    return response


def create_service():
    response = {}

    headers = {}
    headers['Content-Type'] = 'application/json'

    service_payload = {}
    service_payload['resource'] = []
    service1 = {}
    service1['name'] = test_session['name']
    service1['label'] = test_session['name']
    service1['description'] = ''
    service1['is_active'] = True
    service1['type'] = 'sqlite'
    service1['mutable'] = True
    service1['deletable'] = True
    service1['config'] = {}
    service1['config']['database'] = '{}.sqlite'.format(test_session['name'])
    service_payload['resource'].append(service1)
    service_payload = json.dumps(service_payload)

    this_url = '{}system/service?fields=id,name'.format(test_session['base_url'])

    this_auth = ('{}'.format(test_session['admin_user']), '{}'.format(test_session['admin_password']))

    create_service = requests.post(this_url, auth=this_auth, data=service_payload, headers=headers)

    this_json = json.loads(create_service.text)
    response['create_service_status_code'] = create_service.status_code
    response['service_id'] = this_json['resource'][0]['id']
    response['service_name'] = this_json['resource'][0]['name']

    if create_service.status_code == requests.codes.ok:
        print('Service } created.'.format(response['service_name']))
    else:
        print('Service NOT created.')

    return response


def create_table():
    response = {}

    headers = {}
    headers['Content-Type'] = 'application/json'

    table_payload = {"resource": [{"name": "todo", "label": "Todo", "plural": "Todos", "alias": None, "field": [{"name": "id", "label": "Id", "type": "id"}, {"name": "name", "label": "Name", "type": "string", "size": 80, "allow_null": False}, {"name": "complete", "label": "Complete", "type": "boolean", "default": False}]}]}
    table_payload = json.dumps(table_payload)

    this_url = '{}{}/_schema'.format(test_session['base_url'], test_session['service_name'])

    this_auth = ('{}'.format(test_session['admin_user']), '{}'.format(test_session['admin_password']))

    create_table_req = requests.post(this_url, auth=this_auth, data=table_payload, headers=headers)

    this_json = json.loads(create_table_req.text)
    response['create_table_status_code'] = create_table_req.status_code
    response['table_name'] = this_json['resource'][0]['name']

    if create_table_req.status_code == requests.codes.ok:
        print('Table {} created.'.format(response['table_name']))
    else:
        print('Table NOT created.')

    return response


def create_app():
    response = {}

    headers = {}
    headers['Content-Type'] = 'application/json'

    app_payload = {}
    app_payload['resource'] = []
    app1 = {}
    app1['name'] = test_session['name']
    app1['description'] = ''
    app1['type'] = 0
    app1['role_id'] = None
    app1['is_active'] = True
    app_payload['resource'].append(app1)
    app_payload = json.dumps(app_payload)

    this_url = '{}system/app?fields=id,name,api_key'.format(test_session['base_url'])
    this_auth = ('{}'.format(test_session['admin_user']), '{}'.format(test_session['admin_password']))

    create_app = requests.post(this_url, auth=this_auth, data=app_payload, headers=headers)

    this_json = json.loads(create_app.text)
    response['create_app_status_code'] = create_app.status_code
    response['app_id'] = this_json['resource'][0]['id']
    response['app_name'] = this_json['resource'][0]['name']
    response['api_key'] = this_json['resource'][0]['api_key']

    if create_app.status_code == requests.codes.ok:
        print('App {} created.'.format(response['app_name']))
    else:
        print('App NOT created.')

    return response


def create_role():
    response = {}

    headers = {}
    headers['Content-Type'] = 'application/json'

    role_payload = {}
    role_payload['resource'] = []
    role1 = {}
    role1['name'] = test_session['name']
    role1['is_active'] = True
    role1['role_service_access_by_role_id'] = []
    role1access = {}
    role1access['verb_mask'] = 31
    role1access['requestor_mask'] = 1
    role1access['component'] = '*'
    role1access['service_id'] = test_session['service_id']
    role1['role_service_access_by_role_id'].append(role1access)
    role_payload['resource'].append(role1)
    role_payload = json.dumps(role_payload)

    this_url = '{}system/role?fields=id,name'.format(test_session['base_url'])
    this_auth = ('{}'.format(test_session['admin_user']), '{}'.format(test_session['admin_password']))

    create_role = requests.post(this_url, auth=this_auth, data=role_payload, headers=headers)

    this_json = json.loads(create_role.text)
    response['create_role_status_code'] = create_role.status_code
    response['role_id'] = this_json['resource'][0]['id']
    response['role_name'] = this_json['resource'][0]['name']

    if create_role.status_code == requests.codes.ok:
        print('Role {} created.'.format(response['role_name']))
    else:
        print('Role NOT created.')

    return response


def assign_user_to_app_to_role():
    response = {}

    headers = {}
    headers['Content-Type'] = 'application/json'

    relation_payload = {}
    relation_payload['user_to_app_to_role_by_user_id'] = []
    relation1 = {}
    relation1['app_id'] = test_session['app_id']
    relation1['role_id'] = test_session['role_id']
    relation_payload['user_to_app_to_role_by_user_id'].append(relation1)
    relation_payload = json.dumps(relation_payload)

    this_url = '{}system/user/{}?related=user_to_app_to_role_by_user_id'.format(test_session['base_url'], test_session['user_id'])
    this_auth = ('{}'.format(test_session['admin_user']), '{}'.format(test_session['admin_password']))


    assign_relationship = requests.patch(this_url, auth=this_auth, data=relation_payload, headers=headers)

    this_json = json.loads(assign_relationship.text)
    response['assign_relationship_status_code'] = assign_relationship.status_code
    response['relationship_id'] = this_json['user_to_app_to_role_by_user_id'][0]['id']

    if assign_relationship.status_code == requests.codes.ok:
        print('User-App-Role Relationship assigned.')
    else:
        print('User-App-Role Relationship {} assigned.')

    return response


def create_user():
    response = {}

    headers = {}
    headers['Content-Type'] = 'application/json'

    user_payload = {}
    user_payload['resource'] = []
    user1 = {}
    user1['email'] = '{}@example.com'.format(test_session['name'])
    user1['password'] = test_session['password']
    user_payload['resource'].append(user1)
    user_payload = json.dumps(user_payload)

    this_url = '{}system/user?fields=id,email'.format(test_session['base_url'])
    this_auth = ('{}'.format(test_session['admin_user']), '{}'.format(test_session['admin_password']))

    create_user = requests.post(this_url, auth=this_auth, data=user_payload, headers=headers)

    this_json = json.loads(create_user.text)
    response['create_user_status_code'] = create_user.status_code
    response['user_id'] = this_json['resource'][0]['id']
    response['user_email'] = this_json['resource'][0]['email']

    if create_user.status_code == requests.codes.ok:
        print('User {} created.'.format(response['user_email']))
    else:
        print('User NOT created.')

    return response


def create_session():
    session_payload = {}
    session_payload['email'] = test_session['user_email']
    session_payload['password'] = test_session['password']
    session_payload = json.dumps(session_payload)

    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['X-DreamFactory-API-Key'] = test_session['api_key']

    session = requests.post('{}user/session'.format(test_session['base_url']), data=session_payload, headers=headers)

    if session.status_code == requests.codes.ok:
        print('Session created.')
    else:
        print('Session NOT created.')

    return session


def build_record_payload(max_count):
    counter = 1
    db_payload = {}
    db_payload['resource'] = []
    db_record = {}
    while counter < max_count + 1:
        db_record['name'] = 'Test Record {}'.format(counter)
        db_record['complete'] = random.choice([True, False])
        db_payload['resource'].append(db_record)
        counter += 1

    db_payload = json.dumps(db_payload)
    return db_payload


def post_records(db_payload, session_json):
    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['X-DreamFactory-API-Key'] = test_session['api_key']
    headers['X-DreamFactory-Session-Token'] = session_json['session_token']
    db_post = requests.post('{}{}/_table/todo'.format(test_session['base_url'], test_session['service_name']), data=db_payload, headers=headers)

    if db_post.status_code == requests.codes.ok:
        print('Records created.')
    else:
        print('Records NOT created.')

    return db_post


def delete_records(db_post_json, session_json):
    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['X-DreamFactory-API-Key'] = test_session['api_key']
    headers['X-DreamFactory-Session-Token'] = session_json['session_token']
    db_post_json = json.dumps(db_post_json)
    db_delete = requests.delete('{}{}/_table/todo'.format(test_session['base_url'], test_session['service_name']), data=db_post_json, headers=headers)

    if db_delete.status_code == requests.codes.ok:
        print('Records deleted.')
    else:
        print('Records NOT deleted.')


    return db_delete


def delete_session(session_json):
    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['X-DreamFactory-API-Key'] = test_session['api_key']
    headers['X-DreamFactory-Session-Token'] = session_json['session_token']
    session_deleted = requests.delete('{}user/session'.format(test_session['base_url']), headers=headers)

    if session_deleted.status_code == requests.codes.ok:
        print('Session deleted.')
    else:
        print('Session NOT deleted.')


    return session_deleted


def run_test(counter):
    test_result = {}
    test_result['test_number'] = counter
    test_result['status'] = ''
    session = create_session()

    if session.status_code == requests.codes.ok:
        test_result['create_session_status_code'] = session.status_code
        session_json = json.loads(session.text)
        test_result['create_session_token'] = session_json['session_token']
        db_payload = build_record_payload(test_session['record_count'])
        db_post = post_records(db_payload, session_json)

        if db_post.status_code == requests.codes.ok:
            test_result['db_post_status_code'] = db_post.status_code
            db_post_json = json.loads(db_post.text)
            db_delete = delete_records(db_post_json, session_json)

            if db_delete.status_code == requests.codes.ok:
                test_result['db_delete_status_code'] = db_delete.status_code
                session_deleted = delete_session(session_json)

                if session_deleted.status_code == requests.codes.ok:
                    test_result['session_deleted_status_code'] = session_deleted.status_code
                    test_result['status'] = 'Test ran successfully.'
                else:
                    test_result['session_deleted_status_code'] = session_deleted.status_code
                    session_deleted_error_json = json.loads(session_deleted.text)
                    test_result['session_deleted_error'] = session_deleted_error_json['error']['message']
                    test_result['status'] = 'Session Delete Failed.'
            else:
                test_result['db_delete_status_code'] = db_delete.status_code
                db_delete_error_json = json.loads(db_delete.text)
                test_result['db_delete_error'] = db_delete_error_json['error']['message']
                test_result['status'] = 'Record Delete Failed.'
        else:
            test_result['db_post_status_code'] = db_post.status_code
            db_post_error_json = json.loads(db_post.text)
            test_result['db_post_error'] = db_post_error_json['error']['message']
            test_result['status'] = 'Record Post Failed.'
    else:
        test_result['create_session_status_code'] = session.status_code
        session_error_json = json.loads(session.text)
        test_result['create_session_error'] = session_error_json['error']['message']
        test_result['status'] = 'Session Creation Failed'

    return test_result


def run_multiple_tests():
    test_results = []
    counter = 0
    while counter < test_session['test_count']:
        print('Running test #{}'.format(counter))
        test_result = run_test(counter)
        test_results.append(test_result)
        counter += 1
        time.sleep(.5)
    return test_results


def delete_role():
    response = {}

    this_url = '{}system/role/{}'.format(test_session['base_url'], test_session['role_id'])
    this_auth = ('{}'.format(test_session['admin_user']), '{}'.format(test_session['admin_password']))

    delete_role = requests.delete(this_url, auth=this_auth)

    this_json = json.loads(delete_role.text)
    response['delete_role_status_code'] = delete_role.status_code

    if delete_role.status_code == requests.codes.ok:
        print('Role deleted.')
    else:
        print('Role NOT deleted.')

    return response


def delete_user():
    response = {}

    this_url = '{}system/user/{}'.format(test_session['base_url'], test_session['user_id'])
    this_auth = ('{}'.format(test_session['admin_user']), '{}'.format(test_session['admin_password']))

    delete_user = requests.delete(this_url, auth=this_auth)

    this_json = json.loads(delete_user.text)
    response['delete_user_status_code'] = delete_user.status_code

    if delete_user.status_code == requests.codes.ok:
        print('User deleted.')
    else:
        print('User NOT deleted.')

    return response


def delete_app():
    response = {}

    this_url = '{}system/app/{}'.format(test_session['base_url'], test_session['app_id'])
    this_auth = ('{}'.format(test_session['admin_user']), '{}'.format(test_session['admin_password']))

    delete_app = requests.delete(this_url, auth=this_auth)

    this_json = json.loads(delete_app.text)
    response['delete_app_status_code'] = delete_app.status_code

    if delete_app.status_code == requests.codes.ok:
        print('App deleted.')
    else:
        print('App NOT deleted.')

    return response


def delete_service():
    response = {}

    this_url = '{}system/service/{}'.format(test_session['base_url'], test_session['service_id'])
    this_auth = ('{}'.format(test_session['admin_user']), '{}'.format(test_session['admin_password']))

    delete_service = requests.delete(this_url, auth=this_auth)

    this_json = json.loads(delete_service.text)
    response['delete_service_status_code'] = delete_service.status_code

    if delete_service.status_code == requests.codes.ok:
        print('Service deleted.')
    else:
        print('Service NOT deleted.')

    return response


test_session = {}
#test_session['base_url'] = input('What is the base url of the api? (e.g. http://mydf.com/api/v2/)')
test_session['base_url'] = 'http://df.local:8080/api/v2/'
#test_session['admin_user'] = input('What is the admin user\'s email?')
test_session['admin_user'] = 'drew@dreamfactory.com'
#test_session['admin_password'] = input('What is the admin user\'s password?')
test_session['admin_password'] = 'password'
#test_session['test_count'] = input('How many tests would you like to run? ')
test_session['test_count'] = '10'
test_session['test_count'] = int(test_session['test_count'])
#test_session['record_count'] = input('How many records would you like to make per test? ')
test_session['record_count'] = '10'
test_session['record_count'] = int(test_session['record_count'])

print('Generating random username and password.')
rands = generate_rands()
test_session['name'] = rands['name']
test_session['password'] = rands['password']
print('User: {} | Password: {}'.format(test_session['name'], test_session['password']))

print('Creating DB service.')
service = create_service()
test_session['create_service_status_code'] = service['create_service_status_code']
test_session['service_id'] = service['service_id']
test_session['service_name'] = service['service_name']

print('Creating todo table.')
table = create_table()
test_session['create_table_status_code'] = table['create_table_status_code']
test_session['table_name'] = table['table_name']

print('Creating app.')
app = create_app()
test_session['create_app_status_code'] = app['create_app_status_code']
test_session['app_id'] = app['app_id']
test_session['app_name'] = app['app_name']
test_session['api_key'] = app['api_key']

print('Creating role.')
role = create_role()
test_session['create_role_status_code'] = role['create_role_status_code']
test_session['role_id'] = role['role_id']
test_session['role_name'] = role['role_name']

print('Creating user.')
user = create_user()
test_session['create_user_status_code'] = user['create_user_status_code']
test_session['user_id'] = user['user_id']
test_session['user_email'] = user['user_email']

print('Assigning User-App-Role relationship.')
relationship = assign_user_to_app_to_role()
test_session['assign_relationship_status_code'] = relationship['assign_relationship_status_code']
test_session['relationship_id'] = relationship['relationship_id']

print('Commencing tests.')
test_results = run_multiple_tests()
test_session['test_results'] = test_results
print('Tests complete.')

print('Deleting role.')
role_deleted = delete_role()
test_session['delete_role_status_code'] = role_deleted['delete_role_status_code']

print('Deleting user.')
user_deleted = delete_user()
test_session['delete_user_status_code'] = user_deleted['delete_user_status_code']

print('Deleting app.')
app_deleted = delete_app()
test_session['delete_app_status_code'] = app_deleted['delete_app_status_code']

print('Deleting service.')
service_deleted = delete_service()
test_session['delete_service_status_code'] = service_deleted['delete_service_status_code']

pprint(test_session)
