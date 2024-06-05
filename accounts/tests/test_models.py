from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from accounts.models import Department, CustomUser

class ReimbursementModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='employee',
            email='employee@nucleusteq.com',
            password='password123',
            is_employee=True
        )
        self.department = Department.objects.create(name='HR', manager=self.user)
        self.user.department = self.department
        self.user.save()

    def test_reimbursement_creation(self):
        reimbursement = Reimbursement.objects.create(
            employee=self.user,
            category='travel',
            amount=1000,
            description='Business trip to NYC'
        )
        self.assertEqual(reimbursement.status, 'pending')
        self.assertEqual(reimbursement.amount, 1000)
        self.assertEqual(reimbursement.category, 'travel')
        self.assertEqual(reimbursement.description, 'Business trip to NYC')
        self.assertEqual(str(reimbursement), f"{self.user} - Travelling - 1000.00")

    def test_reimbursement_amount_limit(self):
        reimbursement = Reimbursement(
            employee=self.user,
            category='travel',
            amount=20000,  # Exceeds the limit for travel
            description='Business trip to NYC'
        )
        with self.assertRaises(ValidationError) as context:
            reimbursement.clean()
        self.assertIn('Amount exceeds the limit for Travelling category', str(context.exception))

    def test_reimbursement_default_admin(self):
        superuser = get_user_model().objects.create_user(
            username='admin',
            email='admin@nucleusteq.com',
            password='password123',
            is_superuser=True
        )
        reimbursement = Reimbursement.objects.create(
            employee=self.user,
            category='tech_assets',
            amount=1000,
            description='New laptop'
        )
        self.assertEqual(reimbursement.admin, superuser)

    def test_reimbursement_invalid_amount_or_category(self):
        reimbursement = Reimbursement(
            employee=self.user,
            amount=None,
            category=None
        )
        with self.assertRaises(ValidationError) as context:
            reimbursement.clean()
        self.assertIn('Amount and category must not be None', str(context.exception))

class AuditLogModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='employee',
            email='employee@nucleusteq.com',
            password='password123',
            is_employee=True
        )
        self.reimbursement = Reimbursement.objects.create(
            employee=self.user,
            category='travel',
            amount=1000,
            description='Business trip to NYC'
        )

    def test_audit_log_creation(self):
        audit_log = AuditLog.objects.create(
            user=self.user,
            reimbursement=self.reimbursement,
            action='created',
            comments='Initial submission'
        )
        self.assertEqual(audit_log.user, self.user)
        self.assertEqual(audit_log.reimbursement, self.reimbursement)
        self.assertEqual(audit_log.action, 'created')
        self.assertEqual(audit_log.comments, 'Initial submission')
        self.assertEqual(str(audit_log), f"{self.reimbursement} - created by {self.user} at {audit_log.timestamp}")

    def test_audit_log_default_timestamp(self):
        audit_log = AuditLog.objects.create(
            user=self.user,
            reimbursement=self.reimbursement,
            action='created'
        )
        self.assertAlmostEqual(audit_log.timestamp, timezone.now(), delta=timezone.timedelta(seconds=1))
