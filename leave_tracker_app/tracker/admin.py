from django.contrib import admin

from models import Leave, UserProfile, LeaveApplication

admin.site.register(Leave)
admin.site.register(UserProfile)
admin.site.register(LeaveApplication)
