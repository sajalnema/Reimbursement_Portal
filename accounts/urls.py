from django.urls import path
from .views import (
    login_view, signup_view, home_redirect, manage_departments, delete_department, manage_employees, delete_employee,
    logout_view, admin_home, manager_home, delete_employee_confirmation, employee_home, assign_manager, change_role, manager_employees
)
from . import views

app_name = 'accounts'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('home_redirect/', home_redirect, name='home_redirect'),
    path('admin_home/', admin_home, name='admin_home'),
    path('manager_home/', manager_home, name='manager_home'),
    path('employee_home/', employee_home, name='employee_home'),
    path('manage_departments/', manage_departments, name='manage_departments'),
    path('delete_department/<int:pk>/', delete_department, name='delete_department'),
    path('manage_employees/', manage_employees, name='manage_employees'),
    path('delete_employee/<int:pk>/', delete_employee, name='delete_employee'),
    path('logout/', logout_view, name='logout'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('assign_manager/', views.assign_manager, name='assign_manager'),
    path('change_role/', change_role, name='change_role'),
    path('manager_employees/', manager_employees, name='manager_employees'),
    path('delete_employee_confirmation/<int:pk>/', delete_employee_confirmation, name='delete_employee_confirmation'),
]
