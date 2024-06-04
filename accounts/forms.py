from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Department
from .validators import validate_company_email

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_company_email])
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    is_manager = forms.BooleanField(required=False)
    is_employee = forms.BooleanField(required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True, label='Department')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'is_manager', 'is_employee', 'department')
    
    def clean(self):
        cleaned_data = super().clean()
        is_manager = cleaned_data.get("is_manager")
        is_employee = cleaned_data.get("is_employee")

        if is_manager and is_employee:
            raise forms.ValidationError("An employee cannot be both a manager and an employee. Please select only one.")

        if not is_manager and not is_employee:
            raise forms.ValidationError("Please select either manager or employee.")

        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(widget=forms.PasswordInput)

class AssignManagerForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_employee=True), label='Employee')
    manager = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_manager=True), label='Manager')

    def __init__(self, *args, **kwargs):
        super(AssignManagerForm, self).__init__(*args, **kwargs)
        self.fields['manager'].queryset = CustomUser.objects.filter(is_manager=True)
        self.fields['employee'].queryset = CustomUser.objects.filter(is_employee=True)

class PromoteEmployeeForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_employee=True), label='Employee')
