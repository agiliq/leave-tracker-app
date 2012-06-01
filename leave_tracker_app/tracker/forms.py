#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import LeaveApplication


class LeaveApplicationForm(ModelForm):

    class Meta:

        model = LeaveApplication
        exclude = ('status', 'usr')

    def save(self, request, commit=True):
        model = super(LeaveApplicationForm, self).save(commit=False)

        model.usr = request.user.userprofile

        if commit:
            model.save()

        return model


