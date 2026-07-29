from enterprise.legacy_admin.tests import BaseTestCase

class TestAdmin(BaseTestCase):

    def test_admin_dashboard(self):
        response = self.app.get('/admin/dashboard')
        self.assertEqual(response.status_code, 200)
