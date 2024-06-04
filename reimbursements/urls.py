from django.urls import path
from . import views

app_name = 'reimbursements'

urlpatterns = [
    path('', views.reimbursement_list, name='list'),
    path('submit/', views.submit_reimbursement, name='submit'),
    path('approve/<int:pk>/', views.approve_reimbursement, name='approve'),
    path('decline/<int:pk>/', views.approve_reimbursement, name='decline'),  # Use the same view for decline
    path('detail/<int:pk>/', views.reimbursement_detail, name='detail'),
]
