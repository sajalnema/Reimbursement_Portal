from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.utils import redirect_to_dashboard

User = get_user_model()

class UtilsTestCase(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin",
            email="admin@nucleusteq.com",
            password="password123"
        )
        self.manager = User.objects.create_user(
            username="manager",
            email="manager@nucleusteq.com",
            password="password123",
            is_manager=True
        )
        self.employee = User.objects.create_user(
            username="employee",
            email="employee@nucleusteq.com",
            password="password123",
            is_employee=True
        )
        self.anonymous_user = User.objects.create_user(
            username="anonymous",
            email="anonymous@nucleusteq.com",
            password="password123"
        )

    def test_redirect_to_dashboard_superuser(self):
        response = redirect_to_dashboard(self.superuser)
        self.assertEqual(response.url, reverse('accounts:admin_home'))

    def test_redirect_to_dashboard_manager(self):
        response = redirect_to_dashboard(self.manager)
        self.assertEqual(response.url, reverse('accounts:manager_home'))

    def test_redirect_to_dashboard_employee(self):
        response = redirect_to_dashboard(self.employee)
        self.assertEqual(response.url, reverse('accounts:employee_home'))

    def test_redirect_to_dashboard_anonymous_user(self):
        response = redirect_to_dashboard(self.anonymous_user)
        self.assertEqual(response.url, reverse('login'))
