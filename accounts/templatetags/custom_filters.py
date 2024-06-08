from django import template

register = template.Library()

@register.filter
def filter_by_status(reimbursements, status):
    return reimbursements.filter(status=status)

@register.filter
def count_items(queryset):
    return queryset.count()
