from django.test import TestCase
from reimbursements.forms import ReimbursementForm
from reimbursements.models import Reimbursement

class ReimbursementFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {
            'category': 'travel',
            'amount': 100.00,
            'description': 'Travel expenses',
            'document': None
        }
        form = ReimbursementForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_exceeds_category_limit(self):
        form_data = {
            'category': 'travel',
            'amount': 16000.00,  # Exceeds travel limit
            'description': 'Expensive travel expenses',
            'document': None
        }
        form = ReimbursementForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['amount'], ["Amount exceeds the limit for travel category"])
