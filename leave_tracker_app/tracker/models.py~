#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings


class Leave(models.Model):

    type_of_leave = models.CharField(max_length=20)
    number_fo_days = models.IntegerField(max_length=10)

    def __unicode__(self):
        return self.type_of_leave


class UserProfile(models.Model):

    user = models.OneToOneField(User)
    leaves_taken = models.PositiveIntegerField(max_length=10)
    total_leaves = models.PositiveIntegerField(max_length=10)

    def __unicode__(self):
        return self.user.username


def create_user_profile(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs['created']:
        UserProfile.objects.create(user=instance, leaves_taken=0,
                                   total_leaves=settings.LEAVE_CONST)


post_save.connect(create_user_profile, sender=User)


class LeaveApplication(models.Model):

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    usr = models.ForeignKey(UserProfile)
    leave = models.ForeignKey(Leave)
    status = models.BooleanField()
    subject = models.TextField()

    def __unicode__(self):
        return '%s %s' % (self.usr, self.start_date)


def send_approval_mail(sender, **kwargs):
    instance = kwargs['instance']
    recipients = \
        list(User.objects.filter(is_superuser=True).values_list('email'
             , flat=True))
    subject = ''
    email_body = \
        """Starting %s 
                  Ending %s
                  %s""" \
        % (instance.start_date, instance.end_date, instance.subject)
    if kwargs['created']:
        subject = 'Leave Created by %s' % instance.usr.user
    if instance.status == True:
        subject = 'Leave Approved for %s' % instance.usr.user
        recipients.append(instance.usr.user.email)
    send_mail(subject, email_body, 'leave@agiliq.com', recipients,
              fail_silently=False)


post_save.connect(send_approval_mail, sender=LeaveApplication)

