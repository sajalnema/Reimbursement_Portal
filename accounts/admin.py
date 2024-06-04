# accounts/admin.py

from django.contrib import admin
from .models import CustomUser, Department

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_manager', 'manager', 'department']
    list_filter = ['is_manager', 'department']

admin.site.register(Department)
