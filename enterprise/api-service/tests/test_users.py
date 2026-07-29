from enterprise.api_service.tests import BaseTestCase

class TestUsers(BaseTestCase):

    def test_create_user(self):
        response = self.app.post(
            '/users',
            data=json.dumps({
                'username': 'testuser',
                'password': 'testpassword'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], 'User created successfully')
        self.assertEqual(response.status_code, 201)
