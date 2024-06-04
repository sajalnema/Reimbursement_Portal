from django.test import TestCase
from accounts.forms import CustomUserCreationForm, DepartmentForm, LoginForm, AssignManagerForm, PromoteEmployeeForm
from accounts.models import Department, CustomUser

class CustomUserCreationFormTestCase(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='HR')

    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@nucleusteq.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'is_employee': True,
            'is_manager': False,
            'department': self.department.id
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email_domain(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'is_employee': True,
            'is_manager': False,
            'department': self.department.id
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ["Email must be with the domain '@nucleusteq.com'"])

class DepartmentFormTestCase(TestCase):
    def test_valid_department_form(self):
        form_data = {'name': 'Finance'}
        form = DepartmentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_department_form(self):
        form_data = {'name': ''}
        form = DepartmentForm(data=form_data)
        self.assertFalse(form.is_valid())

class LoginFormTestCase(TestCase):
    def test_valid_login_form(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

class AssignManagerFormTestCase(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='HR')
        self.manager = CustomUser.objects.create_user(
            username='manager',
            email='manager@nucleusteq.com',
            password='managerpass',
            is_manager=True,
            department=self.department
        )
        self.employee = CustomUser.objects.create_user(
            username='employee',
            email='employee@nucleusteq.com',
            password='employeepass',
            is_employee=True,
            department=self.department,
            manager=self.manager
        )

    def test_valid_assign_manager_form(self):
        form_data = {
            'employee': self.employee.id,
            'manager': self.manager.id
        }
        form = AssignManagerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_assign_manager_form_without_manager(self):
        form_data = {
            'employee': self.employee.id,
            'manager': ''
        }
        form = AssignManagerForm(data=form_data)
        self.assertFalse(form.is_valid())

class PromoteEmployeeFormTestCase(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='HR')
        self.employee = CustomUser.objects.create_user(
            username='employee',
            email='employee@nucleusteq.com',
            password='employeepass',
            is_employee=True,
            department=self.department
        )

    def test_valid_promote_employee_form(self):
        form_data = {
            'employee': self.employee.id
        }
        form = PromoteEmployeeForm(data=form_data)
        self.assertTrue(form.is_valid())
