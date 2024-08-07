from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from reimbursements.models import Reimbursement, AuditLog
from accounts.models import CustomUser

class ReimbursementModelTest(TestCase):

    def setUp(self):
        self.superuser = CustomUser.objects.create_user(username='admin', email='admin@example.com', password='password', is_superuser=True)
        self.employee = CustomUser.objects.create_user(username='employee', email='employee@example.com', password='password')
        self.manager = CustomUser.objects.create_user(username='manager', email='manager@example.com', password='password', is_manager=True)
        self.reimbursement = Reimbursement.objects.create(
            employee=self.employee,
            admin=self.superuser,
            category='travel',
            amount=1000,
            description='Business trip',
            status='pending',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    def test_reimbursement_creation(self):
        self.assertEqual(self.reimbursement.category, 'travel')
        self.assertEqual(self.reimbursement.amount, 1000)
        self.assertEqual(self.reimbursement.description, 'Business trip')
        self.assertEqual(self.reimbursement.status, 'pending')

    def test_reimbursement_str(self):
        self.assertEqual(str(self.reimbursement), f"{self.employee} - Travelling - 1000")

    def test_reimbursement_default_admin(self):
        reimbursement = Reimbursement.objects.create(
            employee=self.employee,
            category='tech_assets',
            amount=200,
            description='New laptop',
            status='pending',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.assertEqual(reimbursement.admin, self.superuser)

    def test_reimbursement_clean(self):
        with self.assertRaises(ValidationError):
            reimbursement = Reimbursement(
                employee=self.employee,
                category='tech_assets',
                amount=6000,  # exceeds the limit
                description='Expensive tech',
                status='pending',
            )
            reimbursement.clean()

    def test_reimbursement_date_not_null(self):
        reimbursement = Reimbursement.objects.create(
            employee=self.employee,
            category='travel',
            amount=500,
            description='Conference travel',
            status='pending',
        )
        self.assertIsNotNone(reimbursement.date)
    
class AuditLogModelTest(TestCase):

    def setUp(self):
        self.superuser = CustomUser.objects.create_user(username='admin', email='admin@example.com', password='password', is_superuser=True)
        self.employee = CustomUser.objects.create_user(username='employee', email='employee@example.com', password='password')
        self.reimbursement = Reimbursement.objects.create(
            employee=self.employee,
            admin=self.superuser,
            category='travel',
            amount=1000,
            description='Business trip',
            status='pending',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.audit_log = AuditLog.objects.create(
            user=self.superuser,
            reimbursement=self.reimbursement,
            action='created',
            comments='Initial creation',
            timestamp=timezone.now(),
        )

    def test_auditlog_creation(self):
        self.assertEqual(self.audit_log.action, 'created')
        self.assertEqual(self.audit_log.comments, 'Initial creation')
        self.assertEqual(self.audit_log.user, self.superuser)
        self.assertEqual(self.audit_log.reimbursement, self.reimbursement)

    def test_auditlog_str(self):
        self.assertEqual(str(self.audit_log), f"{self.reimbursement} - created by {self.superuser} at {self.audit_log.timestamp}")
