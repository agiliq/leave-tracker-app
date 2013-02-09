#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .forms import LeaveApplicationForm
from .models import LeaveApplication, UserProfile

import json


def index(request):
    current_user = ''
    if request.user.is_authenticated():
        current_user = UserProfile.objects.get(user=request.user)
    return render(request, 'index.html', {'current_user': current_user})


def oidlogout(request):

    logout(request)
    return redirect('/')


@login_required
def all(request):
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


@login_required
@csrf_exempt
def get_prev_leaves(request):
    if 'uid' not in request.GET or not request.is_ajax():
        raise Http404
    uid = request.GET['uid']
    user = get_object_or_404(User, id=uid)
    leaves = LeaveApplication.objects.filter(usr=user).order_by('-start_date')
    res = {}
    for ind, leave in enumerate(leaves):
        if ind > 2:
            break
        res[ind] = {'start_date': str(leave.start_date), 'end_date': str(leave.end_date),
                'leave': str(leave.leave), 'status': str(leave.status),
                'subject': str(leave.subject) }
    return HttpResponse(json.dumps(res), content_type='application/json')



