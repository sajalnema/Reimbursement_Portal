from django.shortcuts import redirect

def redirect_to_dashboard(user):
    if user.is_superuser:
        return redirect('accounts:admin_home')
    elif user.is_manager:
        return redirect('accounts:manager_home')
    elif user.is_employee:
        return redirect('accounts:employee_home')
    else:
        return redirect('login')
