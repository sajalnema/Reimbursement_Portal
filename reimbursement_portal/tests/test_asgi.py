from django.test import SimpleTestCase
from reimbursement_portal.asgi import application

class ASGITests(SimpleTestCase):

    def test_asgi_application(self):
        self.assertIsNotNone(application)
