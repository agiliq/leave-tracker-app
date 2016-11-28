from django.template import Library
from django.db.models import Sum

from leave_tracker.models import LeaveApplication

register = Library()


@register.filter(name='leaves_taken')
def leaves_taken(obj):
    leaves = LeaveApplication.objects.filter(usr=obj)
    leaves_taken = leaves.aggregate(Sum('num_of_days'))['num_of_days__sum']
    return leaves_taken
