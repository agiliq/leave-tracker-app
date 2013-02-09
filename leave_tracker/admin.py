from django.contrib import admin

from .models import LeaveCategory, UserProfile, LeaveApplication

class LeaveAppAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'usr', 'leave_category', 
                    'status', 'subject']


admin.site.register(LeaveCategory)
admin.site.register(UserProfile)
admin.site.register(LeaveApplication, LeaveAppAdmin)
