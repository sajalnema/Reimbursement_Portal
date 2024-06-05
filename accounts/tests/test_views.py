from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Department, CustomUser
from reimbursements.models import Reimbursement
from decimal import Decimal
from datetime import date

User = get_user_model()

class AccountsViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.department = Department.objects.create(name="HR")
        self.employee = CustomUser.objects.create_user(
            username='employee1',
            password='password123',
            department=self.department,
            is_employee=True
        )
        self.manager = CustomUser.objects.create_user(
            username="manager1",
            email="manager1@nucleusteq.com",
            password="password123",
            is_manager=True,
            department=self.department
        )
        self.superuser = CustomUser.objects.create_superuser(
            username="admin",
            email="admin@nucleusteq.com",
            password="password123"
        )
        self.reimbursement = Reimbursement.objects.create(
            employee=self.employee,
            category='travel',
            amount=Decimal('1000.00'),
            description="Business trip",
            date=date.today()
        )

    def test_home_redirect(self):
        self.client.login(username="employee1", password="password123")
        response = self.client.get(reverse('accounts:home_redirect'))
        self.assertEqual(response.status_code, 302)

    def test_login_view_get(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_post(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'employee1',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)

    def test_signup_view_get(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_signup_view_post(self):
        response = self.client.post(reverse('accounts:signup'), {
            'username': 'employee2',
            'email': 'employee2@nucleusteq.com',
            'password1': 'password123',
            'password2': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'is_employee': True,
            'department': self.department.id
        })
        self.assertEqual(response.status_code, 302)  # Ensure successful signup

    def test_logout_view(self):
        self.client.login(username="employee1", password="password123")
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)

    def test_manage_departments_get(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse('accounts:manage_departments'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/manage_departments.html')

    def test_manage_departments_post(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse('accounts:manage_departments'), {
            'name': 'Finance'
        })
        self.assertEqual(response.status_code, 302)

    def test_delete_department(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse('accounts:delete_department', kwargs={'pk': self.department.pk}))
        self.assertEqual(response.status_code, 302)

    def test_manage_employees_get(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse('accounts:manage_employees'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/manage_employees.html')

    def test_manage_employees_post(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse('accounts:manage_employees'), {
            'username': 'employee3',
            'email': 'employee3@nucleusteq.com',
            'password1': 'password123',
            'password2': 'password123',
            'first_name': 'John',
            'last_name': 'Smith',
            'is_employee': True,
            'department': self.department.id
        })
        self.assertEqual(response.status_code, 302)

    def test_delete_employee(self):
        Reimbursement.objects.filter(employee=self.employee).delete()
        response = self.client.post(reverse('accounts:delete_employee', kwargs={'pk': self.employee.pk}))
        self.assertEqual(response.status_code, 302)

    def test_admin_home(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse('accounts:admin_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/admin_home.html')

    def test_manager_home(self):
        self.client.login(username="manager1", password="password123")
        response = self.client.get(reverse('accounts:manager_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/manager_home.html')

    def test_employee_home(self):
        self.client.login(username="employee1", password="password123")
        response = self.client.get(reverse('accounts:employee_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/employee_home.html')

    def test_assign_manager_get(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse('accounts:assign_manager'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/assign_manager.html')

    def test_assign_manager_post(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse('accounts:assign_manager'), {
            'employee_id': self.employee.id,
            'manager_id': self.manager.id
        })
        self.assertEqual(response.status_code, 302)

    def test_change_role(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse('accounts:change_role'), {
            'employee_id': self.employee.id
        })
        self.assertEqual(response.status_code, 302)

    def test_admin_dashboard(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse('accounts:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/admin_dashboard.html')

    def test_manager_dashboard(self):
        self.client.login(username="manager1", password="password123")
        response = self.client.get(reverse('accounts:manager_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/manager_dashboard.html')

    def test_manager_employees(self):
        self.client.login(username="manager1", password="password123")
        response = self.client.get(reverse('accounts:manager_employees'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/manager_employees.html')

    def test_delete_employee_confirmation_get(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse('accounts:delete_employee_confirmation', kwargs={'pk': self.employee.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/delete_employee_confirmation.html')
    
    def test_home_superuser_redirect(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse('accounts:home'))
        self.assertRedirects(response, reverse('accounts:admin_home'))

    def test_home_manager_redirect(self):
        self.client.login(username="manager1", password="password123")
        response = self.client.get(reverse('accounts:home'))
        self.assertRedirects(response, reverse('accounts:manager_home'))

    def test_home_employee_redirect(self):
        self.client.login(username="employee1", password="password123")
        response = self.client.get(reverse('accounts:home'))
        self.assertRedirects(response, reverse('accounts:employee_home'))

    def test_home_unauthenticated_redirect(self):
        response = self.client.get(reverse('accounts:home'))
        self.assertRedirects(response, reverse('accounts:login'))

    def test_register_get(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_register_post_invalid(self):
        response = self.client.post(reverse('accounts:signup'), {
            'username': 'employee2',
            'email': 'employee2@nucleusteq.com',
            'password1': 'password123',
            'password2': 'password',
            'first_name': 'John',
            'last_name': 'Doe',
            'is_employee': True,
            'department': self.department.id
        })
        self.assertEqual(response.status_code, 200)  # Changed to 200 due to form validation failure

    def test_login_invalid(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_assign_manager_invalid(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse('accounts:assign_manager'), {
            'employee_id': 999,
            'manager_id': 999
        })
        self.assertEqual(response.status_code, 404)

    def test_assign_manager_post_without_manager(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse('accounts:assign_manager'), {
            'employee_id': self.employee.id,
            'manager_id': ''
        })
        self.assertEqual(response.status_code, 302)

    def test_delete_employee_confirmation_post(self):
        Reimbursement.objects.filter(employee=self.employee).delete()
        response = self.client.post(reverse('accounts:delete_employee_confirmation', kwargs={'pk': self.employee.pk}))
        self.assertEqual(response.status_code, 302)
