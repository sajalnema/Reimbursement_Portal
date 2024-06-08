from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, Department
from .forms import DepartmentForm, CustomUserCreationForm, LoginForm, AssignManagerForm
from reimbursements.models import Reimbursement
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse 
from django.db.models import Q
from reimbursements.forms import ReimbursementForm 
from .utils import redirect_to_dashboard


import logging  # for application log

logger = logging.getLogger(__name__)  # for application log


@login_required
def home_redirect(request):
    return redirect_to_dashboard(request.user)

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            logger.info(f"Superuser {request.user.username} accessed home view")
            return redirect('accounts:admin_home')
        elif request.user.is_manager:
            logger.info(f"Manager {request.user.username} accessed home view")
            return redirect('accounts:manager_home')
        else:
            logger.info(f"Employee {request.user.username} accessed home view")
            return redirect('accounts:employee_home')
    else:
        logger.info("Unauthenticated access to home view")
        return redirect('login')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            logger.info(f"New user registered: {user.username}")
            return redirect(reverse('accounts:home'))
        else:
            logger.warning(f"Registration form errors: {form.errors}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def is_admin(user):
    return user.is_superuser

def is_manager(user):
    return user.is_manager

def is_employee(user):
    return user.is_employee

def is_employee_or_manager(user):
    return user.is_employee or user.is_manager

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            next_url = request.POST.get('next') or reverse('accounts:home')
            logger.info(f"User {user.username} logged in")
            return redirect(next_url)
        else:
            logger.warning(f"Login form errors: {form.errors}")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form, 'next': request.GET.get('next', '')})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            logger.info(f"User {user.username} signed up")
            return redirect('accounts:home')
        else:
            logger.warning(f"Signup form errors: {form.errors}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def logout_view(request):
    logger.info(f"User {request.user.username} logged out")
    logout(request)
    return redirect('accounts:login')

@login_required
@user_passes_test(is_admin)
def manage_departments(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info("New department added")
            return redirect('accounts:manage_departments')
        else:
            logger.warning(f"Manage departments form errors: {form.errors}")
    else:
        form = DepartmentForm()
    departments = Department.objects.all()
    return render(request, 'accounts/manage_departments.html', {'form': form, 'departments': departments})

@login_required
@user_passes_test(is_admin)
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    logger.info(f"Department {department.name} deleted")
    return redirect('accounts:manage_departments')


@login_required
@user_passes_test(is_admin)
def manage_employees(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info("New employee added")
            return redirect('accounts:manage_employees')
        else:
            logger.warning(f"Manage employees form errors: {form.errors}")
    else:
        form = CustomUserCreationForm()
    
    employees = CustomUser.objects.filter(is_superuser=False)
    managers = CustomUser.objects.filter(is_manager=True)
    
    return render(request, 'accounts/manage_employees.html', {
        'form': form,
        'employees': employees,
        'managers': managers
    })
@login_required
@user_passes_test(is_admin)
def delete_employee(request, pk):
    employee = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        Reimbursement.objects.filter(employee=employee).delete()

        employee.delete()
        logger.info(f"Employee {employee.username} deleted")
        return redirect('accounts:manage_employees')
    return render(request, 'accounts/delete_employee_confirmation.html', {'employee': employee})

@login_required
@user_passes_test(is_admin)
def admin_home(request):
    logger.debug(f"Admin home accessed by {request.user.username}, superuser status: {request.user.is_superuser}")
    if not request.user.is_superuser:
        logger.warning(f"Access denied for non-superuser {request.user.username}")
        return redirect('accounts:login')

    search_query = request.GET.get('search', '')
    employees = CustomUser.objects.filter(is_employee=True)
    managers = CustomUser.objects.filter(is_manager=True)

    # Fetch reimbursement requests assigned to the admin or from employees without managers
    reimbursements = Reimbursement.objects.filter(
        Q(employee__manager__isnull=True)
    )
    
    if search_query:
        employees = employees.filter(
            Q(username__icontains=search_query) | 
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query)
        )
        logger.info(f"Search query '{search_query}' applied")

    # Calculate reimbursement counts
    total_reimbursements = reimbursements.count()
    approved_reimbursements = reimbursements.filter(status='approved').count()
    declined_reimbursements = reimbursements.filter(status='declined').count()
    pending_reimbursements = reimbursements.filter(status='pending').count()

    return render(request, 'accounts/admin_home.html', {
        'employees': employees,
        'managers': managers,
        'reimbursements': reimbursements,
        'search_query': search_query,
        'total_reimbursements': total_reimbursements,
        'approved_reimbursements': approved_reimbursements,
        'declined_reimbursements': declined_reimbursements,
        'pending_reimbursements': pending_reimbursements,
    })


@login_required
@user_passes_test(is_manager)
def manager_home(request):
    managed_employees = CustomUser.objects.filter(manager=request.user)
    employee_reimbursements = Reimbursement.objects.filter(employee__in=managed_employees)
    manager_reimbursements = Reimbursement.objects.filter(employee=request.user)
    # Calculate reimbursement counts
    total_reimbursements = employee_reimbursements.count()
    approved_reimbursements = employee_reimbursements.filter(status='approved').count()
    declined_reimbursements = employee_reimbursements.filter(status='declined').count()
    pending_reimbursements = employee_reimbursements.filter(status='pending').count()

    if request.method == 'POST':
        form = ReimbursementForm(request.POST, request.FILES)
        if form.is_valid():
            reimbursement = form.save(commit=False)
            reimbursement.employee = request.user
            reimbursement.save()
            return redirect('accounts:manager_home')
    else:
        form = ReimbursementForm()

      
    return render(request, 'accounts/manager_home.html', {
        'managed_employees': managed_employees,
        'employee_reimbursements': employee_reimbursements,
        'manager_reimbursements': manager_reimbursements,
        'form': form,
        'total_reimbursements': total_reimbursements,
        'approved_reimbursements': approved_reimbursements,
        'declined_reimbursements': declined_reimbursements,
        'pending_reimbursements': pending_reimbursements,
    })

@login_required
def employee_home(request):
    reimbursements = Reimbursement.objects.filter(employee=request.user)
    manager = request.user.manager if request.user.manager else CustomUser.objects.filter(is_superuser=True).first()
    logger.info(f"Employee {request.user.username} accessed home view with {len(reimbursements)} reimbursements")
    return render(request, 'accounts/employee_home.html', {'reimbursements': reimbursements, 'manager': manager})
@login_required
@user_passes_test(is_admin)
def assign_manager(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        manager_id = request.POST.get('manager_id')
        employee = get_object_or_404(CustomUser, id=employee_id)
        if manager_id:
            manager = get_object_or_404(CustomUser, id=manager_id)
        else:
            manager = CustomUser.objects.filter(is_superuser=True).first()
        employee.manager = manager
        employee.save()

        # Update reimbursements where the employee's manager was null
        reimbursements = Reimbursement.objects.filter(employee=employee)
        for reimbursement in reimbursements:
            reimbursement.employee.manager = manager
            reimbursement.save()

        logger.info(f"Manager {manager.username} assigned to employee {employee.username}")
        return redirect('accounts:admin_home')
    else:
        form = AssignManagerForm()
    return render(request, 'accounts/assign_manager.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def change_role(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        employee = get_object_or_404(CustomUser, id=employee_id)
        employee.is_manager = True
        employee.is_employee = False
        employee.save()
        logger.info(f"Employee {employee.username} promoted to manager")
        return redirect('accounts:admin_home')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    managers = CustomUser.objects.filter(is_manager=True)
    logger.info("Admin accessed dashboard")
    return render(request, 'accounts/admin_dashboard.html', {'managers': managers})

@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    manager = request.user
    employees = manager.subordinates.all()
    logger.info(f"Manager {manager.username} accessed dashboard")
    return render(request, 'accounts/manager_dashboard.html', {'manager': manager, 'employees': employees})

@login_required
@user_passes_test(is_manager)
def manager_employees(request):
    manager = request.user
    employees = CustomUser.objects.filter(manager=manager)
    return render(request, 'accounts/manager_employees.html', {'employees': employees})

@login_required
@user_passes_test(is_admin)
def delete_employee_confirmation(request, pk):
    employee = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('accounts:manage_employees')
    return render(request, 'accounts/delete_employee_confirmation.html', {'employee': employee})

@login_required
@user_passes_test(is_employee_or_manager)
def approve_reimbursement(request, pk):
    reimbursement = get_object_or_404(Reimbursement, pk=pk)
    
    logger.debug(f"User {request.user.username} attempting to approve reimbursement ID {pk}")
    logger.debug(f"User authenticated: {request.user.is_authenticated}")
    logger.debug(f"User superuser status: {request.user.is_superuser}")
    logger.debug(f"Reimbursement employee manager: {reimbursement.employee.manager}")

    if not (request.user.is_superuser or reimbursement.employee.manager == request.user):
        logger.warning(f"Access denied for user {request.user.username}")
        return redirect('reimbursements:list')

    if request.method == 'POST':
        action = request.POST.get('action')
        reimbursement.manager_comments = request.POST.get('manager_comments', '')
        if action == 'approve':
            reimbursement.status = 'approved'
        elif action == 'decline':
            reimbursement.status = 'declined'
        reimbursement.save()
        logger.info(f"Reimbursement ID {pk} {action}d by user {request.user.username}")

        if request.user.is_superuser:
            return redirect('accounts:admin_home')
        elif request.user.is_manager:
            return redirect('accounts:manager_home')

    return render(request, 'reimbursements/approve_reimbursement.html', {'reimbursement': reimbursement})

@login_required
@user_passes_test(is_employee_or_manager)
def decline_reimbursement(request, pk):
    reimbursement = get_object_or_404(Reimbursement, pk=pk)
    
    logger.debug(f"User {request.user.username} attempting to decline reimbursement ID {pk}")
    logger.debug(f"User authenticated: {request.user.is_authenticated}")
    logger.debug(f"User superuser status: {request.user.is_superuser}")
    logger.debug(f"Reimbursement employee manager: {reimbursement.employee.manager}")

    if not (request.user.is_superuser or reimbursement.employee.manager == request.user):
        logger.warning(f"Access denied for user {request.user.username}")
        return redirect('reimbursements:list')

    if request.method == 'POST':
        reimbursement.status = 'declined'
        reimbursement.manager_comments = request.POST.get('manager_comments', '')
        reimbursement.save()
        logger.info(f"Reimbursement ID {pk} declined by user {request.user.username}")

        if request.user.is_superuser:
            return redirect('accounts:admin_home')
        elif request.user.is_manager:
            return redirect('accounts:manager_home')

    return render(request, 'reimbursements/approve_reimbursement.html', {'reimbursement': reimbursement})