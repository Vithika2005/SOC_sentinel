from enterprise.auth_service.tests import BaseTestCase

class TestLogin(BaseTestCase):

    def test_invalid_credentials(self):
        response = self.app.post(
            '/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'wrongpassword'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], 'Invalid credentials')
        self.assertEqual(response.status_code, 401)

    def test_valid_credentials(self):
        with app.app_context():
            new_user = User(username='testuser', password='testpassword')
            self.db.session.add(new_user)
            self.db.session.commit()

        response = self.app.post(
            '/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'testpassword'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(isinstance(data['token'], str))
        self.assertEqual(response.status_code, 200)
