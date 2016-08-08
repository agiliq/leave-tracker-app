from django.contrib import admin

from .models import Employee, Payroll, Skill, Department


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # list_display = ('employee_id', 'gender', 'marital_status',
                    # 'job_title', 'date_of_birth', 'phone', 'created_date')
    # list_filter = ('employee_id', 'phone')
    search_fields = ['employee_id', 'phone']
    view_on_site = False


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    # list_display = ('employee', 'account_number', 'gross_salary')
    # list_filter = ('employee__employee_id', 'account_number', 'gross_salary')
    search_fields = ['employee__employee_id', 'account_number', 'gross_salary']
    view_on_site = False

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code']
    view_on_site = False

# @admin.register(Department)
# class DepartmentAdmin(admin.ModelAdmin):
#     search_fields = ['name', 'code']
#     view_on_site = False

# admin.site.register(Employee, EmployeeAdmin)
# admin.site.register(Payroll, PayrollAdmin)