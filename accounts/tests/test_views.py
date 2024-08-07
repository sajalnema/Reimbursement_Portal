from django.test import TestCase, Client
from django.urls import reverse, resolve
from accounts.models import CustomUser, Department
from accounts.views import home, register, login_view, manage_departments, manage_employees, admin_home, manager_home, employee_home
from django.contrib.auth import get_user_model

class AccountsViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.department = Department.objects.create(name="HR")
        self.admin_user = CustomUser.objects.create_superuser(username='admin', email='admin@nucleusteq.com', password='adminpass')
        self.manager_user = CustomUser.objects.create_user(username='manager', email='manager@nucleusteq.com', password='managerpass', is_manager=True, department=self.department)
        self.employee_user = CustomUser.objects.create_user(username='employee', email='employee@nucleusteq.com', password='employeepass', is_employee=True, department=self.department)
        
    def test_home_url_is_resolved(self):
        url = reverse('accounts:home')
        self.assertEquals(resolve(url).func, home)

    def test_register_view_get(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_register_view_post(self):
        response = self.client.post(reverse('accounts:signup'), {
            'username': 'newuser',
            'email': 'newuser@nucleusteq.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'password123',
            'password2': 'password123',
            'is_manager': False,
            'is_employee': True,
            'department': self.department.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:home'))

    def test_login_view_get(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_post(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'employee',
            'password': 'employeepass',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:home'))

    def test_manage_departments_get(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('accounts:manage_departments'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/manage_departments.html')

    def test_manage_employees_get(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('accounts:manage_employees'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/manage_employees.html')

    def test_admin_home(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('accounts:admin_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/admin_home.html')

    def test_manager_home(self):
        self.client.login(username='manager', password='managerpass')
        response = self.client.get(reverse('accounts:manager_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/manager_home.html')

    def test_employee_home(self):
        self.client.login(username='employee', password='employeepass')
        response = self.client.get(reverse('accounts:employee_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/employee_home.html')
