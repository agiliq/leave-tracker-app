from django.contrib import admin

from .models import Employee, Payroll, Skill, Department, Designation


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('code', 'title')
    list_filter = ('code', 'title')
    search_fields = ['code', 'title']
    view_on_site = False

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('code', 'name')
    search_fields = ['code', 'name']
    view_on_site = False

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'gender', 'marital_status',
                    'job_title', 'date_of_birth', 'phone', 'created_date')
    list_filter = ('employee_id', 'phone')
    search_fields = ['employee_id', 'phone']
    view_on_site = False


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'account_number', 'gross_salary')
    list_filter = ('employee__employee_id', 'account_number', 'gross_salary')
    search_fields = ['employee__user_profile__user__first_name', 'employee__user_profile__user__last_name', 'employee__employee_id', 'account_number', 'gross_salary']
    view_on_site = False
    actions = ['send_payslips']

    def send_payslips(self, request, queryset):
        queryset.update(status='p')
    send_payslips.short_description = "Send payslips to selected users"

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('technology_name',)
    search_fields = ['technology_name']
    view_on_site = False
