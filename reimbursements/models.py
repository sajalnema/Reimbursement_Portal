from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from accounts.models import CustomUser

class Reimbursement(models.Model):
    CATEGORY_CHOICES = [
        ('travel', 'Travelling'),
        ('relocation', 'Re-location'),
        ('tech_assets', 'Tech Assets'),
    ]
    CATEGORY_LIMITS = {
        'travel': 15000,
        'relocation': 20000,
        'tech_assets': 5000,
    }
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]
    
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reimbursements')
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='admin_reimbursements', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='travel')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default='No description provided')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    manager_comments = models.TextField(blank=True, null=True)
    date = models.DateField(null=True, blank=True)  # Ensure this line is present

    @property
    def department_manager(self):
        return self.employee.department.manager if self.employee.department else None
    
    def clean(self):
        if self.amount is None or self.category is None:
            raise ValidationError("Amount and category must not be None")
        
        if self.amount > self.CATEGORY_LIMITS.get(self.category, 0):
            raise ValidationError(f"Amount exceeds the limit for {self.get_category_display()} category")
    
    def save(self, *args, **kwargs):
        if not self.admin:
            self.admin = CustomUser.objects.filter(is_superuser=True).first()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.employee} - {self.get_category_display()} - {self.amount}"

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('deleted', 'Deleted'),
        ('accessed', 'Accessed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    reimbursement = models.ForeignKey('Reimbursement', on_delete=models.CASCADE, related_name='audit_logs', null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, default='accessed')
    timestamp = models.DateTimeField(default=timezone.now)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.reimbursement} - {self.action} by {self.user} at {self.timestamp}"
