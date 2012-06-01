from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from forms import LeaveApplicationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from models import LeaveApplication, UserProfile, Leave

def index(request):
    current_user = ""
    if request.user.is_authenticated():
        current_user = UserProfile.objects.get(user = request.user)
    return render(request, "index.html", {"current_user":current_user})


def aclogout(request):

    logout(request)
    return redirect("/")


def aclogin(request):
    redirect_to = request.REQUEST.get('next', '/')
    form = AuthenticationForm(data=request.POST or None)
    if request.POST and form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(redirect_to)
            else:
                return HttpResponse('disabled account')
        else:
            return HttpResponse('invalid login')
    else:
        return render(request, "index.html", {"form":form})

@login_required
def detail(request):
    obj = LeaveApplication.objects.all()
    return render(request, "detail.html", {"obj":obj})

@login_required
def personal(request):
    obj = LeaveApplication.objects.filter(usr__user__username=request.user)
    return render(request, "detail.html", {"obj":obj})

@login_required 
def apply(request):
    form = LeaveApplicationForm(data=request.POST or None)
    
    if form.is_valid():
        form.save(request)
        return redirect(reverse("personal"))
    return render(request, 'index.html', {'form':form})
