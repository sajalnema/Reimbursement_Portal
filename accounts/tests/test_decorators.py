from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from accounts.decorators import manager_required, employee_required

User = get_user_model()

class DecoratorsTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.manager = User.objects.create_user(
            username='manager',
            email='manager@nucleusteq.com',
            password='password123',
            is_manager=True
        )
        self.employee = User.objects.create_user(
            username='employee',
            email='employee@nucleusteq.com',
            password='password123',
            is_employee=True
        )
        self.other_user = User.objects.create_user(
            username='other',
            email='other@nucleusteq.com',
            password='password123'
        )

    def test_manager_required_decorator_allows_manager(self):
        request = self.factory.get('/')
        request.user = self.manager

        @manager_required
        def view(request):
            return 'Access granted'

        response = view(request)
        self.assertEqual(response, 'Access granted')

    def test_manager_required_decorator_denies_non_manager(self):
        request = self.factory.get('/')
        request.user = self.other_user

        @manager_required
        def view(request):
            return 'Access granted'

        with self.assertRaises(PermissionDenied):
            view(request)

    def test_employee_required_decorator_allows_employee(self):
        request = self.factory.get('/')
        request.user = self.employee

        @employee_required
        def view(request):
            return 'Access granted'

        response = view(request)
        self.assertEqual(response, 'Access granted')

    def test_employee_required_decorator_denies_non_employee(self):
        request = self.factory.get('/')
        request.user = self.other_user

        @employee_required
        def view(request):
            return 'Access granted'

        with self.assertRaises(PermissionDenied):
            view(request)
