from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_departments')

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    email = models.EmailField(max_length=254, unique=True)

    def save(self, *args, **kwargs):
        if self.is_manager and not self.manager:
            self.manager = CustomUser.objects.filter(is_superuser=True).first()
        super().save(*args, **kwargs)

        
    def promote_to_manager(self):
        self.is_manager = True
        self.is_employee = False
        self.save()

        
    def __str__(self):
        return self.username
    

class Reimbursement(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    document = models.ImageField(upload_to='documents/')
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manager_comments = models.TextField(null=True, blank=True)
   

    def __str__(self):
        return f"{self.category} - {self.amount}"
