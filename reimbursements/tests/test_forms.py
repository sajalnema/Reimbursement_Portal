from django.test import TestCase
from reimbursements.forms import ReimbursementForm
from reimbursements.models import Reimbursement

class ReimbursementFormTest(TestCase):

    def test_valid_form(self):
        data = {
            'category': 'travel',
            'amount': 500,
            'description': 'Travel expenses',
            'date': '2024-06-16',
        }
        form = ReimbursementForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_exceeds_limit(self):
        data = {
            'category': 'travel',
            'amount': 16000,  # exceeds the limit of 15000 for travel
            'description': 'Expensive travel expenses',
            'date': '2024-06-16',
        }
        form = ReimbursementForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)

    def test_invalid_form_missing_category(self):
        data = {
            'amount': 500,
            'description': 'Travel expenses',
            'date': '2024-06-16',
        }
        form = ReimbursementForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)
