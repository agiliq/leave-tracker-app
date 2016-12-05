from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

from .models import UserProfile

from utils import get_payslip


def index(request):
    user_profile = ''
    if request.user.is_authenticated():
        user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'payroll/payroll.html',
                  {'user_profile': user_profile, 'timezone': timezone.now().strftime("%B")})


def generate_payslip(request):
    user_profile = UserProfile.objects.get(user=request.user)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="payslip.pdf"'
    payslip = get_payslip(user_profile)
    response.write(payslip)
    return response
