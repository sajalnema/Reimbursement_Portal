from django.core.exceptions import ValidationError

def validate_company_email(value):
   
    if not value.endswith('@nucleusteq.com'):
        raise ValidationError('Email must be a valid nucleusteq.com email address.')



