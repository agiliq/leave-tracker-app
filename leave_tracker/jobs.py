from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail


def send_reminder_mail_job(obj):
    subject = "Leave Reminder for %s" % obj.usr
    email_body = """<p>This is a reminder email to notify that you have taken the
                 leave starting from today . </p>
                 Details:
                 Start Date : %s <br>
                 End Date : %s <br>
                 Status : %s <br>
                 Description : %s""" % \
                 (str(obj.start_date)[:10], str(obj.end_date)[:10],
                 obj.status_display, obj.subject)
    recipients = \
        list(User.objects.filter(is_superuser=True).
             values_list('email', flat=True))
    recipients.append(obj.usr.user.email)
    send_mail(subject, email_body, settings.DEFAULT_FROM_EMAIL, recipients,
              fail_silently=False)







