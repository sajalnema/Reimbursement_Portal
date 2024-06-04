import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reimbursement, AuditLog

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Reimbursement)
def log_reimbursement_save(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    AuditLog.objects.create(
        user=instance.employee,
        reimbursement=instance,
        action=action,
        comments=f"Reimbursement {action} by {instance.employee}"
    )
    logger.debug(f"AuditLog created: {action} by {instance.employee} for reimbursement {instance.id}")

@receiver(post_delete, sender=Reimbursement)
def log_reimbursement_delete(sender, instance, **kwargs):
    AuditLog.objects.create(
        user=instance.employee,
        reimbursement=instance,
        action='deleted',
        comments=f"Reimbursement deleted by {instance.employee}"
    )
    logger.debug(f"AuditLog created: deleted by {instance.employee} for reimbursement {instance.id}")


#for sudit log