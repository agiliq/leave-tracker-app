from django.contrib import admin

from .models import Leave, UserProfile, LeaveApplication

class LeaveAppAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'usr', 'leave', 'status', 'subject']

admin.site.register(Leave)
admin.site.register(UserProfile)
admin.site.register(LeaveApplication, LeaveAppAdmin)
