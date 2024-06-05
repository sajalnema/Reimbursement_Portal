# reimbursements/tests/test_models.py

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from reimbursements.models import Reimbursement, AuditLog
from accounts.models import CustomUser, Department
from decimal import Decimal
from datetime import date
from accounts.models import Department, CustomUser

class ReimbursementModelTest(TestCase):

    def setUp(self):
        self.department = Department.objects.create(name="HR")
        self.employee = CustomUser.objects.create_user(
            username="employee1",
            email="employee1@nucleusteq.com",
            password="password123",
            is_employee=True,
            department=self.department
        )
        self.superuser = CustomUser.objects.create_superuser(
            username="admin",
            email="admin@nucleusteq.com",
            password="password123"
        )

    def test_reimbursement_creation(self):
        reimbursement = Reimbursement.objects.create(
            employee=self.employee,
            category='travel',
            amount=Decimal('1000.00'),
            description="Business trip",
            document=None,
            date=date.today()
        )
        self.assertEqual(str(reimbursement), f"{self.employee} - Travelling - 1000.00")

    def test_reimbursement_amount_limit(self):
        reimbursement = Reimbursement(
            employee=self.employee,
            category='travel',
            amount=Decimal('20000.00'),  # Exceeds limit
            description="Luxury trip",
            document=None,
            date=date.today()
        )
        with self.assertRaises(ValidationError):
            reimbursement.clean()

    def test_reimbursement_default_admin(self):
        reimbursement = Reimbursement.objects.create(
            employee=self.employee,
            category='travel',
            amount=Decimal('1000.00'),
            description="Business trip",
            document=None,
            date=date.today()
        )
        self.assertEqual(reimbursement.admin, self.superuser)

    def test_reimbursement_without_amount_or_category(self):
        reimbursement = Reimbursement(
            employee=self.employee,
            description="No amount or category",
            document=None,
            date=date.today()
        )
        with self.assertRaises(ValidationError):
            reimbursement.clean()

    def test_audit_log_creation(self):
        reimbursement = Reimbursement.objects.create(
            employee=self.employee,
            category='travel',
            amount=Decimal('1000.00'),
            description="Business trip",
            document=None,
            date=date.today()
        )
        audit_log = AuditLog.objects.create(
            user=self.employee,
            reimbursement=reimbursement,
            action='created',
            comments="Initial creation"
        )
        self.assertEqual(str(audit_log), f"{reimbursement} - created by {self.employee} at {audit_log.timestamp}")

class AuditLogModelTest(TestCase):

    def setUp(self):
        self.employee = CustomUser.objects.create_user(
            username="employee1",
            email="employee1@nucleusteq.com",
            password="password123",
            is_employee=True
        )
        self.reimbursement = Reimbursement.objects.create(
            employee=self.employee,
            category='travel',
            amount=Decimal('1000.00'),
            description="Business trip",
            document=None,
            date=date.today()
        )

    def test_audit_log_creation(self):
        audit_log = AuditLog.objects.create(
            user=self.employee,
            reimbursement=self.reimbursement,
            action='created',
            comments="Initial creation"
        )
        self.assertEqual(str(audit_log), f"{self.reimbursement} - created by {self.employee} at {audit_log.timestamp}")
