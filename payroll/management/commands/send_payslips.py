from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings
from django.template import loader, Context

from payroll.models import Payroll
from payroll.utils import get_payslip, send_an_email

class Command(BaseCommand):
    help = 'Send payslips at the end of the month'

    def handle(self, *args, **options):
        queryset = Payroll.objects.all()
        for payroll in queryset:
            subject = "Payslip for the month of {0}".format(
                timezone.now().strftime("%B"))
            email_template = loader.get_template('payroll/email/payslip.html')
            context = {'first_name': payroll.employee.user_profile.user.first_name, 'last_name': payroll.employee.user_profile.user.last_name, 'month': timezone.now().strftime("%B")}
            message = email_template.render(context)
            user_profile = payroll.employee.user_profile
            payslip = get_payslip(user_profile)
            send_an_email(subject, message, settings.LEAVE_TRACKER_RECIPIENT, [
                          payroll.employee.user_profile.user.email], payslip)