#for audit log


from django.utils.deprecation import MiddlewareMixin
from .models import AuditLog

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            AuditLog.objects.create(
                user=request.user,
                action='accessed',
                comments=f"Accessed {request.path} from IP {request.META['REMOTE_ADDR']}",
                reimbursement=None  # explicitly set reimbursement to None
            )
        return None
