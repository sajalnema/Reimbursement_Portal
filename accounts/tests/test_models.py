from django.test import TestCase
from accounts.models import CustomUser, Department
from reimbursements.models import Reimbursement
from django.core.exceptions import ValidationError 

class DepartmentModelTestCase(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='HR')

    def test_department_creation(self):
        self.assertEqual(self.department.name, 'HR')

    def test_department_str(self):
        self.assertEqual(str(self.department), 'HR')

class CustomUserModelTestCase(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='HR')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@nucleusteq.com',
            password='testpass',
            department=self.department,
            is_employee=True
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@nucleusteq.com')
        self.assertEqual(self.user.department.name, 'HR')
        self.assertTrue(self.user.is_employee)
        self.assertFalse(self.user.is_manager)

    def test_promote_to_manager(self):
        self.user.promote_to_manager()
        self.assertTrue(self.user.is_manager)
        self.assertFalse(self.user.is_employee)

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_manager_assignment(self):
        manager = CustomUser.objects.create_user(
            username='manager',
            email='manager@nucleusteq.com',
            password='managerpass',
            is_superuser=True,
            is_staff=True
        )
        employee = CustomUser.objects.create_user(
            username='employee',
            email='employee@nucleusteq.com',
            password='employeepass',
            is_employee=True
        )
        employee.promote_to_manager()
        self.assertEqual(employee.manager, manager)

class ReimbursementModelTestCase(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='HR')
        self.employee = CustomUser.objects.create_user(
            username='employee',
            email='employee@nucleusteq.com',
            password='employeepass',
            department=self.department,
            is_employee=True
        )
        self.reimbursement = Reimbursement.objects.create(
            employee=self.employee,
            category='travel',
            amount=100.00,
            description='Travel expenses'
        )

    def test_reimbursement_creation(self):
        self.assertEqual(self.reimbursement.employee.username, 'employee')
        self.assertEqual(self.reimbursement.category, 'travel')
        self.assertEqual(self.reimbursement.amount, 100.00)
        self.assertEqual(self.reimbursement.description, 'Travel expenses')
        self.assertEqual(self.reimbursement.status, 'pending')

    def test_reimbursement_exceeds_category_limit(self):
        reimbursement = Reimbursement(
            employee=self.employee,
            category='travel',
            amount=16000.00,  # Exceeds travel limit
            description='Expensive travel expenses'
        )
        with self.assertRaises(ValidationError):
            reimbursement.clean()

    def test_reimbursement_without_amount_or_category(self):
        reimbursement = Reimbursement(employee=self.employee, description='No amount or category')
        with self.assertRaises(ValidationError):
            reimbursement.clean()
