from django.apps import AppConfig


class ReimbursementsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reimbursements"
#for audit log
class ReimbursementsConfig(AppConfig):
    name = 'reimbursements'

    def ready(self):
        import reimbursements.signals