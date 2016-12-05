from django.template import Template, Context
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.utils import timezone

# Third party imports
from io import BytesIO
from reportlab.pdfgen import canvas
import pdfcrowd

import os


def send_an_email(subject, body, from_email, to_emails, attachment=None):
    email = EmailMessage()
    email.subject = subject
    email.body = body
    email.from_email = from_email
    email.to = to_emails
    if attachment:
        # email.attach_file(attachment)
        email.attach('payslip.pdf', attachment, 'application/pdf')
    email.send()


def get_payslip(user_profile):
    template_file = os.path.join(
        settings.PROJECT_DIR, os.path.pardir, "payroll/templates/payroll/payroll.html")
    template = Template(open(template_file, 'rb').read())
    context = Context({'user_profile': user_profile,
                       'timezone': timezone.now().strftime("%B")})
    html = template.render(context)
    try:
        client = pdfcrowd.Client(
            settings.PDF_USERNAME, settings.PDF_KEY)
        pdf = client.convertHtml(html.encode("utf-8"))
    except pdfcrowd.Error, why:
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
    return pdf
