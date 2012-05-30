from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


class Leave(models.Model):

    type_of_leave = models.CharField(max_length=20)
    number_fo_days = models.IntegerField(max_length=10)

    def __unicode__(self):
        return self.type_of_leave

    
class UserProfile(models.Model):

    user = models.OneToOneField(User)
    leaves_taken = models.IntegerField(max_length=10)
    total_leaves = models.IntegerField(max_length=10)
    
    def __unicode__(self):
        return self.user.username
        
class LeaveApplication(models.Model):

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    usr = models.ForeignKey(UserProfile)
    leave = models.ForeignKey(Leave)
    status = models.BooleanField()
    subject = models.TextField()
    
    def __unicode__(self):
        return "%s %s" %(self.usr, self.start_date)


