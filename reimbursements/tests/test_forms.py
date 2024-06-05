from django.test import TestCase
from reimbursements.forms import ReimbursementForm
from reimbursements.models import Reimbursement
from decimal import Decimal
from datetime import date

class ReimbursementFormTests(TestCase):

    def test_reimbursement_form_valid_data(self):
        form_data = {
            'category': 'travel',
            'amount': 1000.00,
            'description': 'Business trip',
            'date': date.today()
        }
        form = ReimbursementForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_reimbursement_form_exceeds_amount_limit(self):
        form_data = {
            'category': 'travel',
            'amount': 20000.00,  # Exceeds the limit for 'travel'
            'description': 'Business trip',
            'date': date.today()
        }
        form = ReimbursementForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)
        self.assertEqual(form.errors['amount'], ["Amount exceeds the limit for travel category"])

    def test_reimbursement_form_missing_category(self):
        form_data = {
            'amount': 1000.00,
            'description': 'Business trip',
            'date': date.today()
        }
        form = ReimbursementForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)

    def test_reimbursement_form_missing_amount(self):
        form_data = {
            'category': 'travel',
            'description': 'Business trip',
            'date': date.today()
        }
        form = ReimbursementForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)

    def test_reimbursement_form_missing_description(self):
        form_data = {
            'category': 'travel',
            'amount': 1000.00,
            'date': date.today()
        }
        form = ReimbursementForm(data=form_data)
        self.assertTrue(form.is_valid())  # Description is optional, so the form should be valid
