# reimbursements/forms.py

from django import forms
from .models import Reimbursement


class ReimbursementForm(forms.ModelForm):
    class Meta:
        model = Reimbursement
        fields = ['category', 'amount', 'description', 'document', 'date']  # Include date field

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        category = self.cleaned_data.get('category')
        if amount > Reimbursement.CATEGORY_LIMITS[category]:
            raise forms.ValidationError(f"Amount exceeds the limit for {category} category")
        return amount