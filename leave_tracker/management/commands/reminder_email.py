from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

from leave_tracker.models import LeaveApplication

from datetime import datetime


class Command(BaseCommand):
    help = 'Sends email to people if start_date is that day(of execution of this command)'

    def handle(self, *args, **kwargs):
        print 'Send reminder_email mangement command started'
        today = datetime.today().date()
        leaves = LeaveApplication.objects.filter(start_date=today)
        admin_recipients = \
            list(User.objects.filter(is_superuser=True).
                 values_list('email', flat=True))
        for obj in leaves:
            subject = "Leave reminder for %s" % obj.usr
            email_body = """<p>This is a reminder email to notify that you have taken the
                        leave starting from today . </p>
                        Details:
                        Start Date : %s <br>
                        End Date : %s <br>
                        Status : %s <br>
                        Description : %s""" % \
                (str(obj.start_date)[:10], str(obj.end_date)[:10],
                 obj.status_display, obj.subject)
            recipients = admin_recipients
            recipients.append(obj.usr.user.email)
            send_mail(subject, email_body, settings.DEFAULT_FROM_EMAIL, recipients,
                      fail_silently=False)
