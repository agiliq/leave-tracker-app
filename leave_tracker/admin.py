from django.contrib import admin

from .models import LeaveCategory, UserProfile, LeaveApplication

def approve_multiple(modeladmin, request, queryset):
        queryset.update(status=True)

approve_multiple.short_description = "Approve All"

class LeaveAppAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'usr', 'leave_category', 
                    'status', 'subject']
    actions = [approve_multiple]

def approve_multiple(modeladmin, request, queryset):
        for leave in queryset:
            leave.status=True
            leave.save()


admin.site.register(LeaveCategory)
admin.site.register(UserProfile)
admin.site.register(LeaveApplication, LeaveAppAdmin)
