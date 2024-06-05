from django.test import TestCase, Client
from reimbursements.middleware import SomeCustomMiddleware

class SomeCustomMiddlewareTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_middleware_behavior(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
