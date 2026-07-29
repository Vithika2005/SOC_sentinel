import unittest

from enterprise.api_service.app import app, db
from enterprise.api_service.models import User, Order

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
