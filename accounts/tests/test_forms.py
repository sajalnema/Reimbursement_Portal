from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.forms import (
    DepartmentForm, 
    CustomUserCreationForm, 
    LoginForm, 
    AssignManagerForm, 
    PromoteEmployeeForm
)
from accounts.models import Department, CustomUser
from accounts.forms import ReimbursementForm
from reimbursements.models import Reimbursement
from datetime import date
from accounts.forms import UserRegistrationForm

class DepartmentFormTest(TestCase):

    def test_department_form_valid(self):
        form = DepartmentForm(data={'name': 'HR'})
        self.assertTrue(form.is_valid())

    def test_department_form_invalid(self):
        form = DepartmentForm(data={'name': ''})
        self.assertFalse(form.is_valid())

class CustomUserCreationFormTest(TestCase):

    def setUp(self):
        self.department = Department.objects.create(name='HR')

    def test_custom_user_creation_form_valid(self):
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'email': 'test@nucleusteq.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_manager': False,
            'is_employee': True,
            'password1': 'password123',
            'password2': 'password123',
            'department': self.department.id
        })
        self.assertTrue(form.is_valid())

    def test_custom_user_creation_form_invalid_email(self):
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'email': 'test@gmail.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_manager': False,
            'is_employee': True,
            'password1': 'password123',
            'password2': 'password123',
            'department': self.department.id
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Email must be a valid nucleusteq.com email address.'])

    def test_custom_user_creation_form_invalid_password_mismatch(self):
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'email': 'test@nucleusteq.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_manager': False,
            'is_employee': True,
            'password1': 'password123',
            'password2': 'differentpassword',
            'department': self.department.id
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ["The two password fields didn't match."])

    def test_custom_user_creation_form_invalid_role(self):
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'email': 'test@nucleusteq.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_manager': True,
            'is_employee': True,
            'password1': 'password123',
            'password2': 'password123',
            'department': self.department.id
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ['An employee cannot be both a manager and an employee. Please select only one.'])

    def test_custom_user_creation_form_no_role(self):
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'email': 'test@nucleusteq.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_manager': False,
            'is_employee': False,
            'password1': 'password123',
            'password2': 'password123',
            'department': self.department.id
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ['Please select either manager or employee.'])

class LoginFormTest(TestCase):

    def test_login_form_valid(self):
        form = LoginForm(data={'username': 'testuser', 'password': 'password123'})
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form = LoginForm(data={'username': '', 'password': ''})
        self.assertFalse(form.is_valid())

class AssignManagerFormTest(TestCase):

    def setUp(self):
        self.manager = CustomUser.objects.create_user(
            username='manager',
            email='manager@nucleusteq.com',
            password='password123',
            is_manager=True
        )
        self.employee = CustomUser.objects.create_user(
            username='employee',
            email='employee@nucleusteq.com',
            password='password123',
            is_employee=True
        )

    def test_assign_manager_form_valid(self):
        form = AssignManagerForm(data={'employee': self.employee.id, 'manager': self.manager.id})
        self.assertTrue(form.is_valid())

    def test_assign_manager_form_invalid(self):
        form = AssignManagerForm(data={'employee': '', 'manager': ''})
        self.assertFalse(form.is_valid())

class PromoteEmployeeFormTest(TestCase):

    def setUp(self):
        self.employee = CustomUser.objects.create_user(
            username='employee',
            email='employee@nucleusteq.com',
            password='password123',
            is_employee=True
        )

    def test_promote_employee_form_valid(self):
        form = PromoteEmployeeForm(data={'employee': self.employee.id})
        self.assertTrue(form.is_valid())

    def test_promote_employee_form_invalid(self):
        form = PromoteEmployeeForm(data={'employee': ''})
        self.assertFalse(form.is_valid())
        
class ReimbursementFormTests(TestCase):
    def test_reimbursement_form_missing_category(self):
        form_data = {
            'amount': 100.00,
            'description': 'Business trip to New York',
            'date': date.today()
        }
        form = ReimbursementForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)


class UserRegistrationFormTests(TestCase):

    def test_registration_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'differentpassword',
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ["The two password fields didn’t match."])

    def test_registration_form_common_password(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'password123',
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ["This password is too common."])