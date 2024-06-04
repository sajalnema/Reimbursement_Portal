# accounts/decorators.py

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def manager_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_manager:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def employee_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_employee:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap