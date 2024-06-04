from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from reimbursements.models import Reimbursement, AuditLog
from accounts.models import CustomUser, Department

class ReimbursementModelTestCase(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='HR')
        self.employee = CustomUser.objects.create_user(
            username='employee',
            email='employee@nucleusteq.com',
            password='employeepass',
            is_employee=True,
            department=self.department
        )

    def test_reimbursement_creation(self):
        reimbursement = Reimbursement.objects.create(
            employee=self.employee,
            category='travel',
            amount=100.00,
            description='Travel expenses'
        )
        self.assertEqual(reimbursement.employee.username, 'employee')
        self.assertEqual(reimbursement.category, 'travel')
        self.assertEqual(reimbursement.amount, 100.00)
        self.assertEqual(reimbursement.description, 'Travel expenses')
        self.assertEqual(reimbursement.status, 'pending')

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

class AuditLogModelTestCase(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='HR')
        self.employee = CustomUser.objects.create_user(
            username='employee',
            email='employee@nucleusteq.com',
            password='employeepass',
            is_employee=True,
            department=self.department
        )
        self.reimbursement = Reimbursement.objects.create(
            employee=self.employee,
            category='travel',
            amount=100.00,
            description='Travel expenses'
        )
        self.admin = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@nucleusteq.com',
            password='adminpass'
        )

    def test_auditlog_creation(self):
        auditlog = AuditLog.objects.create(
            user=self.admin,
            reimbursement=self.reimbursement,
            action='created',
            comments='Initial creation'
        )
        self.assertEqual(auditlog.user.username, 'admin')
        self.assertEqual(auditlog.reimbursement, self.reimbursement)
        self.assertEqual(auditlog.action, 'created')
        self.assertEqual(auditlog.comments, 'Initial creation')
