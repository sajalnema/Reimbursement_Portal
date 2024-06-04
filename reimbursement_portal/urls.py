from django.contrib import admin
from django.urls import path, include
from accounts.views import home  # Import the home view
from django.contrib.auth import views as auth_views

# For static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('reimbursements/', include('reimbursements.urls', namespace='reimbursements')),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', home, name='home'),  # Add this line to map the root URL to the home view
]

# Static files (media)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
