#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.validators import MaxValueValidator

from datetime import timedelta


class LeaveCategory(models.Model):
    "The type of leaves. Eg Casual leave, medical leave"
    type_of_leave = models.CharField(max_length=20)
    number_of_days = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999999999)])

    class Meta:
        verbose_name_plural = "Leave Categories"

    def __unicode__(self):
        return self.type_of_leave


class UserProfile(models.Model):
    "Data we need for a user"
    user = models.OneToOneField(User)
    total_leaves = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999999999)])

    def __unicode__(self):
        return self.user.username

    def user_display(self):
        if self.user.first_name and self.user.last_name:
            return "%s %s" % (self.user.first_name, self.user.last_name)
        elif self.user.first_name:
            return self.user.first_name
        elif self.user.last_name:
            return self.user.last_name
        else:
            return self.user.username


def create_user_profile(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs['created']:
        UserProfile.objects.create(user=instance,
                                   total_leaves=settings.LEAVE_CONST)


post_save.connect(create_user_profile, sender=User)


class LeaveApplication(models.Model):
    "A leave request"
    start_date = models.DateField()
    end_date = models.DateField()
    num_of_days = models.IntegerField()
    usr = models.ForeignKey(UserProfile)
    leave_category = models.ForeignKey("LeaveCategory")
    status = models.BooleanField(default=False)
    subject = models.TextField()

    def __unicode__(self):
        return '%s %s' % (self.usr, self.start_date)

    @property
    def user(self):
        return self.usr

    @property
    def status_display(self):
        if self.status:
            return "Approved"
        else:
            return "Requested"


def send_approval_mail(sender, **kwargs):
    instance = kwargs['instance']
    recipients = [settings.LEAVE_TRACKER_RECIPIENT]
    subject = None

    if kwargs['created']:
        email_body = render_to_string('leave_tracker/leave_created.txt',
                                      {"leave": instance})
        subject = 'Leave Created by %s' % instance.usr.user
        recipients.append(instance.usr.user.email)
        send_mail(subject, email_body, settings.LEAVE_TRACKER_FROM_MAIL, recipients,
                  fail_silently=False)
    if instance.status:
        email_body = render_to_string('leave_tracker/leave_approved.txt',
                                      {"leave": instance})
        subject = 'Leave Approved for %s' % instance.usr.user
        recipients.append(instance.usr.user.email)
        send_mail(subject, email_body, settings.LEAVE_TRACKER_FROM_MAIL, recipients,
                  fail_silently=False)


post_save.connect(send_approval_mail, sender=LeaveApplication)


def modify_num_of_days(sender, **kwargs):
    "Calculate num_of_days from start_date, end_date excluding weekends"
    holidays = settings.WEEKEND_HOLIDAYS
    instance = kwargs['instance']
    start = instance.start_date
    end = instance.end_date
    dg = (start + timedelta(x + 1) for x in xrange((end - start).days))
    s = sum(1 for day in dg if day.weekday() not in holidays)
    if start.weekday() < 5:
        s += 1
    instance.num_of_days = s


def change_username(sender, **kwargs):
    "Since we get username via openid, they can be duplicate"
    instance = kwargs['instance']
    if instance.username[0:6] == 'openid':
        instance.username = instance.email[0:-11]
    "Taken from django_openid_auth"
    i = 1
    while True:
        if i > 1:
            instance.username += str(i)
        count = User.objects.filter(
            username__exact=instance.username).exclude(pk=instance.pk)
        if not count:
            break
        i += 1

pre_save.connect(change_username, sender=User)
pre_save.connect(modify_num_of_days, sender=LeaveApplication)
