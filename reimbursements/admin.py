from django.contrib import admin
from .models import Reimbursement, AuditLog

admin.site.register(Reimbursement)


#for audit log

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'reimbursement', 'action', 'timestamp', 'comments')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'reimbursement__id', 'comments')