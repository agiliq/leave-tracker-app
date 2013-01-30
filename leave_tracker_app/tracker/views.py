#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from forms import LeaveApplicationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from models import LeaveApplication, UserProfile, Leave


def index(request):
    current_user = ''
    if request.user.is_authenticated():
        current_user = UserProfile.objects.get(user=request.user)
    return render(request, 'index.html', {'current_user': current_user})


def oidlogout(request):

    logout(request)
    return redirect('/')


@login_required
def detail(request):
    current_user = ''
    obj = LeaveApplication.objects.all()
    current_user = UserProfile.objects.get(user=request.user)
    return render(request, 'detail.html', {'obj': obj, 'current_user': current_user})


@login_required
def personal(request):
    current_user = ''
    obj = \
        LeaveApplication.objects.filter(usr__user=request.user)
    current_user = UserProfile.objects.get(user=request.user)
    return render(request, 'detail.html', {'obj': obj, 'current_user': current_user})


@login_required
def apply(request):
    form = LeaveApplicationForm(data=request.POST or None)

    if form.is_valid():
        form.save(request)
        return redirect(reverse('personal'))
    current_user = ''
    if request.user.is_authenticated():
        current_user = UserProfile.objects.get(user=request.user)
    return render(request, 'index.html', {'form': form, 'current_user': current_user}, )
