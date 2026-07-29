import unittest

from enterprise.legacy_admin.app import app, db
from enterprise.legacy_admin.models import User, Order

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.db = db
        with app.app_context():
            self.db.create_all()

    def tearDown(self):
        with app.app_context():
            self.db.session.remove()
            self.db.drop_all()

class UserTest(BaseTestCase):
    def test_create_user(self):
        response = self.client.post('/users', json={'username': 'user1', 'password': 'pass123'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User user1 created successfully', response.data)

class OrderTest(BaseTestCase):
    def test_create_order(self):
        response = self.client.post('/orders', json={'user_id': 1, 'product': 'Product A', 'quantity': 1})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Order created successfully', response.data)
