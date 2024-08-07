from django.test import TestCase
from accounts.forms import CustomUserCreationForm, DepartmentForm

class FormsTestCase(TestCase):
    def test_custom_user_creation_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@nucleusteq.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'password123',
            'password2': 'password123',
            'is_manager': False,
            'is_employee': True,
            'department': 1,  # Ensure this department exists in your test database
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors.as_data())

    def test_custom_user_creation_form_invalid(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@nucleusteq.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'password123',
            'password2': 'password123',
            'is_manager': True,
            'is_employee': True,  # This should cause validation error
            'department': 1,
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('is_manager', form.errors)
        self.assertIn('is_employee', form.errors)

    def test_department_form_valid(self):
        form_data = {
            'name': 'IT'
        }
        form = DepartmentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_department_form_invalid(self):
        form_data = {
            'name': ''
        }
        form = DepartmentForm(data=form_data)
        self.assertFalse(form.is_valid())
