from django.shortcuts import render
from .models import UserProfile

def index(request):
    current_user = ''
    if request.user.is_authenticated():
        current_user = UserProfile.objects.get(user=request.user)
    return render(request, 'payroll/payroll.html',
                  {'current_user': current_user})
