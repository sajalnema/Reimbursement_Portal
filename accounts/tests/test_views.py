from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser, Department
from reimbursements.models import Reimbursement

class AccountsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.department = Department.objects.create(name='HR')
        self.superuser = CustomUser.objects.create_superuser(
            username='admin', email='admin@nucleusteq.com', password='adminpass'
        )
        self.manager = CustomUser.objects.create_user(
            username='manager', email='manager@nucleusteq.com', password='managerpass', is_manager=True, department=self.department
        )
        self.employee = CustomUser.objects.create_user(
            username='employee', email='employee@nucleusteq.com', password='employeepass', is_employee=True, department=self.department, manager=self.manager
        )

    def test_home_view_redirect(self):
        response = self.client.get(reverse('accounts:home'))
        self.assertRedirects(response, reverse('login'))

    def test_register_view(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'newuser@nucleusteq.com',
            'password1': 'newuserpassword',
            'password2': 'newuserpassword',
            'first_name': 'New',
            'last_name': 'User',
            'is_employee': True,
            'department': self.department.id
        })
        self.assertRedirects(response, reverse('accounts:home'))

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

        response = self.client.post(reverse('login'), {
            'username': 'employee',
            'password': 'employeepass'
        })
        self.assertRedirects(response, reverse('accounts:home'))

    def test_logout_view(self):
        self.client.login(username='employee', password='employeepass')
        response = self.client.get(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('accounts:login'))

    def test_manage_departments_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('accounts:manage_departments'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/manage_departments.html')

        response = self.client.post(reverse('accounts:manage_departments'), {
            'name': 'Finance'
        })
        self.assertRedirects(response, reverse('accounts:manage_departments'))

    def test_delete_department_view(self):
        self.client.login(username='admin', password='adminpass')
        department = Department.objects.create(name='IT')
        response = self.client.post(reverse('accounts:delete_department', args=[department.id]))
        self.assertRedirects(response, reverse('accounts:manage_departments'))

    def test_manage_employees_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('accounts:manage_employees'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/manage_employees.html')

        response = self.client.post(reverse('accounts:manage_employees'), {
            'username': 'newemployee',
            'email': 'newemployee@nucleusteq.com',
            'password1': 'newemployeepass',
            'password2': 'newemployeepass',
            'first_name': 'New',
            'last_name': 'Employee',
            'is_employee': True,
            'department': self.department.id
        })
        self.assertRedirects(response, reverse('accounts:manage_employees'))

    def test_delete_employee_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('accounts:delete_employee', args=[self.employee.id]))
        self.assertRedirects(response, reverse('accounts:manage_employees'))

    def test_admin_home_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('accounts:admin_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/admin_home.html')

    def test_manager_home_view(self):
        self.client.login(username='manager', password='managerpass')
        response = self.client.get(reverse('accounts:manager_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/manager_home.html')

    def test_employee_home_view(self):
        self.client.login(username='employee', password='employeepass')
        response = self.client.get(reverse('accounts:employee_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/employee_home.html')

    def test_assign_manager_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('accounts:assign_manager'), {
            'employee_id': self.employee.id,
            'manager_id': self.manager.id
        })
        self.assertRedirects(response, reverse('accounts:admin_home'))

    def test_change_role_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('accounts:change_role'), {
            'employee_id': self.employee.id
        })
        self.assertRedirects(response, reverse('accounts:admin_home'))

    def test_admin_dashboard_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('accounts:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/admin_dashboard.html')

    def test_manager_dashboard_view(self):
        self.client.login(username='manager', password='managerpass')
        response = self.client.get(reverse('accounts:manager_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/manager_dashboard.html')
