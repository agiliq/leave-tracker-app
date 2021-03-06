#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from parsley.decorators import parsleyfy

from .models import LeaveApplication


@parsleyfy
class LeaveApplicationForm(ModelForm):

    class Meta:

        model = LeaveApplication
        fields = ('start_date', 'end_date', 'leave_category', 'subject')

    def save(self, request, commit=True):
        model = super(LeaveApplicationForm, self).save(commit=False)

        model.usr = request.user.userprofile

        if commit:
            model.save()

        return model

    def clean_end_date(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if end_date >= start_date:
            return end_date
        else:
            raise forms.ValidationError("'End Date' should be "
                                        "after 'Start Date' .")
