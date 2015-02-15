import os
import unittest
import tempfile

import users
import app
import json

from db import DB

# The bcrypt hashing process was making the tests run slowly so I've statically set the data to save time
# test_create_users still hits the bcrypt code path
hashed_passwords = [
    "$2a$08$Q/Uyh6LbKLnx1qn0LOUEyuh0nO4ajeyZ4YPNe//u36pGT0ayvlFTm", #user1
    "$2a$08$fcZvJHIIoORXQ6w1.yl.YeBWGOsfR59.GNVRIH8uNHoY9V2FU1OpC", #user2
    "$2a$08$40EMkiugtTVeDd8.PYrthestcGmpKpSI4pXbD.X4GM5c1EDBP60xC", #user3
]

test_users = [{'id': str(n), 'username': 'user%s' % n, 'email': 'user%s@internet.com' % n, 'password': hashed_passwords[n - 1]} for n in range(1, 4)]

# All the tests are prefixed with test. I think this is a bit ugly but makes the unittests standard library
# pick them up. I could use pytest but I wanted to avoid the extra dependency to make running the tests easy.
class UserTest(unittest.TestCase):
    def setUp(self):
        self.user_service = app.app

        self.db_file, self.user_service.config['DATABASE'] = tempfile.mkstemp()
        self.db = DB(self.user_service.config['DATABASE'], app.bcrypt)
        users.init_db(self.db, self.user_service)
        [self.db.write('insert into users values(:id, :username, :email, :password)', user) for user in test_users]

        self.user_service.config['TESTING'] = True
        self.app = self.user_service.test_client()

    def tearDown(self):
        os.close(self.db_file)
        os.unlink(self.user_service.config['DATABASE'])

    def create_user(self, user):
        user_json = json.dumps(user._asdict())
        
        return json.loads(raw_resp.data)

    def test_create_user(self):
        user_json = json.dumps({'username': 'test_user', 'email': 'test@test.com', 'password': '1234'})

        headers = [('Content-Type', 'application/json')]
        raw_resp = self.app.post('/users', headers = headers, data = user_json)
        resp = json.loads(raw_resp.data)

        self.assertEquals('test_user', resp['username'])
        self.assertEquals('test@test.com', resp['email'])
        self.assertIn('id', resp)
        self.assertNotIn('password', resp)

        hashed_password = self.db.read_all('select password from users where id = :id', {'id': resp['id']})[0][0]
        self.assertTrue(self.db.secure_hash_verify(hashed_password, '1234'), 'hashed password did not match password')

    def test_list_users(self):
        raw_resp = self.app.get('/users')
        resp_data = json.loads(raw_resp.data)

        self.assertIn('users', resp_data)
        users = resp_data['users']

        self.assertEquals(3, len(users))
        for n in range(0, 3):
            expected_user = test_users[n]
            actual_user = users[n]

            self.assertEquals(expected_user['id'], actual_user['id'])
            self.assertEquals(expected_user['username'], actual_user['username'])
            self.assertEquals(expected_user['email'], actual_user['email'])

    def test_list_user(self):
        raw_resp = self.app.get('/users/1')

        expected_user = test_users[0]
        actual_user = json.loads(raw_resp.data)

        self.assertEquals(expected_user['id'], actual_user['id'])
        self.assertEquals(expected_user['username'], actual_user['username'])
        self.assertEquals(expected_user['email'], actual_user['email'])
        

    def test_delete_user(self):
        headers = [('foobar', self.user_service.config['VALID_API_KEY'])]
        raw_resp = self.app.delete('/users/1', headers = headers)
        
        resp = json.loads(raw_resp.data)
        self.assertEquals('deleted', resp['message'])

    def test_fail_creating_user_with_existing_username(self):
        user_json = json.dumps({'username': 'user1', 'email': 'test@test.com', 'password': '1234'})

        headers = [('Content-Type', 'application/json')]
        raw_resp = self.app.post('/users', headers = headers, data = user_json)
        resp = json.loads(raw_resp.data)

        self.assertEquals(400, raw_resp.status_code)
        self.assertEquals('User user1 already exists', resp['message'])

    def test_fail_creating_user_with_missing_fields(self):
        user_json = json.dumps({'email': 'test@test.com', 'password': '1234'})

        headers = [('Content-Type', 'application/json')]
        raw_resp = self.app.post('/users', headers = headers, data = user_json)
        resp = json.loads(raw_resp.data)

        self.assertEquals(400, raw_resp.status_code)
        self.assertEquals('Expected username, email and password. Got password, email', resp['message'])

    def test_fail_listing_user_that_does_not_exist(self):
        raw_resp = self.app.get('/users/notreal')

        self.assertEquals(404, raw_resp.status_code)

    def test_fail_deleting_user_that_does_not_exist(self):
        headers = [('foobar', self.user_service.config['VALID_API_KEY'])]
        raw_resp = self.app.delete('/users/notreal', headers = headers)
        
        self.assertEquals(404, raw_resp.status_code)

    def test_fail_deleting_user_without_api_key(self):
        raw_resp = self.app.delete('/users/1')
        resp = json.loads(raw_resp.data)

        self.assertEquals(401, raw_resp.status_code)
        self.assertEquals('Missing or invalid foobar API key header', resp['message'])

    def test_fail_deleting_user_without_correct_api_key(self):
        headers = [('foobar', 'bad_api_key_value')]
        raw_resp = self.app.delete('/users/1', headers = headers)
        resp = json.loads(raw_resp.data)

        self.assertEquals(401, raw_resp.status_code)
        self.assertEquals('Missing or invalid foobar API key header', resp['message'])

if __name__ == '__main__':
    unittest.main()