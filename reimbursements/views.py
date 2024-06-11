from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404 
from .forms import ReimbursementForm
from .models import Reimbursement
from accounts.models import CustomUser
import logging
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ValidationError , ObjectDoesNotExist
from django.http import HttpResponseServerError


logger = logging.getLogger(__name__)

def is_manager(user):
    return user.is_manager

def is_employee(user):
    return user.is_employee

def is_employee_or_manager(user):
    return user.is_employee or user.is_manager or user.is_superuser

@login_required
def submit_reimbursement(request):
    if request.method == 'POST':
        form = ReimbursementForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                reimbursement = form.save(commit=False)
                reimbursement.employee = request.user
                reimbursement.created_at = timezone.now()  # Ensure created_at is set to current time
                reimbursement.updated_at = timezone.now()
                reimbursement.date = form.cleaned_data.get('date')
                reimbursement.save()
                messages.success(request, 'Reimbursement submitted successfully.')
                logger.info(f"Reimbursement submitted by {request.user.username}")
                return redirect('accounts:employee_home')
            else:
                messages.error(request, 'Form is not valid. Please correct the errors.')
        except ValidationError as e:
            messages.error(request, f'Validation error: {e}')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')
            return HttpResponseServerError()
    else:
        form = ReimbursementForm()
    return render(request, 'reimbursements/submit_reimbursement.html', {'form': form})

@login_required
def reimbursement_list(request):
    if request.user.is_superuser:
        reimbursements = Reimbursement.objects.all()
    elif request.user.is_manager:
        managed_employees = CustomUser.objects.filter(manager=request.user)
        reimbursements = Reimbursement.objects.filter(employee__in=managed_employees)
    else:
        reimbursements = Reimbursement.objects.filter(employee=request.user)
    
    context = {
        'reimbursements': reimbursements,
        'is_superuser': request.user.is_superuser,
        'is_manager': request.user.is_manager
    }
    
    return render(request, 'reimbursements/reimbursement_list.html', context)

@login_required
@user_passes_test(is_employee_or_manager)
def reimbursement_detail(request, pk):
    reimbursement = get_object_or_404(Reimbursement, pk=pk)
    
    # Check if the user is authorized to view the reimbursement
    if not (
        request.user.is_superuser or 
        reimbursement.employee.manager == request.user or 
        reimbursement.employee == request.user or 
        (reimbursement.employee.manager is None and reimbursement.employee.department.manager == request.user)
    ):
        return redirect('accounts:manager_home')  # Prevent unauthorized access
    
    if request.method == 'POST':
        action = request.POST.get('action')
        reimbursement.manager_comments = request.POST.get('manager_comments', '')
        if action == 'approve':
            reimbursement.status = 'approved'
        elif action == 'decline':
            reimbursement.status = 'declined'
        reimbursement.save()
        
        if request.user.is_superuser:
            return redirect('accounts:admin_home')
        elif request.user.is_manager:
            return redirect('accounts:manager_home')
    
    return render(request, 'reimbursements/reimbursement_detail.html', {'reimbursement': reimbursement})

@login_required
@user_passes_test(is_employee_or_manager)
def approve_reimbursement(request, pk):

    try: 
        reimbursement = get_object_or_404(Reimbursement, pk=pk)
        if not (request.user.is_superuser or 
            (reimbursement.employee.manager == request.user and reimbursement.employee.department == request.user.department)):
            messages.warning(request, 'You do not have permission to approve this reimbursement.')
            return redirect('reimbursements:list')

        if request.method == 'POST':
            action = request.POST.get('action')
            reimbursement.manager_comments = request.POST.get('manager_comments', '')
            reimbursement.date = request.POST.get('date')  
            if action == 'approve':
                reimbursement.status = 'approved'
                messages.success(request, 'Reimbursement approved successfully.')
           
            elif action == 'decline':
                reimbursement.status = 'declined'
                messages.success(request, 'Reimbursement declined successfully.')
       
            reimbursement.updated_at = timezone.now()
            reimbursement.save()

            if request.user.is_superuser:
                return redirect('accounts:admin_home')
            elif request.user.is_manager:
                return redirect('accounts:manager_home')
        
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return HttpResponseServerError()
    return render(request, 'reimbursements/approve_reimbursement.html', {'reimbursement': reimbursement})


@login_required
@user_passes_test(is_employee_or_manager)
def decline_reimbursement(request, pk):
    try:
        reimbursement = get_object_or_404(Reimbursement, pk=pk)
    except ObjectDoesNotExist:
         messages.error(request, 'Reimbursement not found.')
         return redirect('reimbursements:list')

    if not (request.user.is_superuser or reimbursement.employee.manager == request.user):
        print("Access denied: User is not authorized.")
        messages.warning(request, 'You do not have permission to decline this reimbursement.')
        return redirect('reimbursements:list')

    if request.method == 'POST':
        try:
            reimbursement.status = 'declined'
            reimbursement.manager_comments = request.POST.get('manager_comments', '')
            reimbursement.updated_at = timezone.now()
            reimbursement.save()
            messages.success(request, 'Reimbursement declined successfully.')
            logger.info(f"Reimbursement ID {pk} declined by user {request.user.username}")

            print(f"Reimbursement declined with comments: {reimbursement.manager_comments}")

            if request.user.is_superuser:
                return redirect('accounts:admin_home')
            elif request.user.is_manager:
                return redirect('accounts:manager_home')
        except Exception as e:
            messages.error(request, 'An unexpected error occurred. Please try again later.')
            logger.error(f"Unexpected error when declining reimbursement: {e}")

        return render(request, 'reimbursements/approve_reimbursement.html', {'reimbursement': reimbursement})

    def redirect_back_to_dashboard(request):
        if request.user.is_superuser:
            return redirect('accounts:admin_home')
        elif request.user.is_manager:
            return redirect('accounts:manager_home')
        else:
            return redirect('accounts:employee_home')
