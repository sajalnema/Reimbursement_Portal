from django.test import SimpleTestCase
from reimbursement_portal.wsgi import application

class WSGITests(SimpleTestCase):

    def test_wsgi_application(self):
        self.assertIsNotNone(application)

