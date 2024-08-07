from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.validators import validate_company_email

class ValidatorsTestCase(TestCase):

    def test_validate_company_email_valid(self):
        try:
            validate_company_email('user@nucleusteq.com')
        except ValidationError:
            self.fail('validate_company_email() raised ValidationError unexpectedly!')

    def test_validate_company_email_invalid(self):
        with self.assertRaises(ValidationError):
            validate_company_email('user@example.com')
