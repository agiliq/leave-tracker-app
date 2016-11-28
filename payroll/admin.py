# Django imports
from django.contrib import admin
from django.conf import settings

# Local imports
from .models import Employee, Payroll, Skill, Department, Designation
from utils import get_payslip, send_an_email

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('code', 'title')
    list_filter = ('code', 'title')
    search_fields = ['code', 'title']
    view_on_site = False
    empty_value_display = '-empty-'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('code', 'name')
    search_fields = ['code', 'name']
    view_on_site = False
    empty_value_display = '-empty-'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'employee_id', 'gender', 'marital_status',
                    'job_title', 'date_of_birth', 'phone', 'created_date')
    list_filter = ('employee_id', 'phone')
    search_fields = ['employee_id', 'user_profile__user__first_name',
                     'user_profile__user__last_name', 'user_profile__user__email', 'phone']
    view_on_site = False
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'

    def employee_name(self, obj):
        return "{0} {1}".format(obj.user_profile.user.first_name, obj.user_profile.user.last_name)
    employee_name.short_description = 'Employee Name'


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'account_number', 'gross_salary', 'net_salary')
    list_filter = ('employee__employee_id', 'account_number')
    search_fields = ['employee__user_profile__user__email', 'employee__user_profile__user__first_name',
                     'employee__user_profile__user__last_name', 'employee__employee_id', 'account_number', 'gross_salary']
    view_on_site = False
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_select_related = ('employee',)
    readonly_fields = ('net_salary',)
    save_as = True
    save_on_top = True
    actions = ['send_payslips']

    def net_salary(self, obj):
        deductions = obj.income_tax + obj.professional_tax + \
            obj.pf_employee + obj.pf_employer + obj.other_charges
        gross_salary = obj.gross_salary
        net_salary = gross_salary - deductions
        return net_salary
    net_salary.short_description = 'Net Salary'

    def send_payslips(self, request, queryset):
        subject = "Payslip for the month of "
        message = """
        Dear {0} {1},

        Please find the payslip attached to this mail.

        Thank You,
        Agiliq Team
        """.format(request.user.first_name, request.user.last_name)
        for payroll in queryset:
            user_profile = payroll.employee.user_profile
            payslip = get_payslip(user_profile)
            send_an_email(subject, message, settings.LEAVE_TRACKER_RECIPIENT, [request.user.email], payslip)
        self.message_user(
            request, "Payslips sent to selected employees successfully.")
    send_payslips.short_description = "Send payslips to selected users"


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('technology_name',)
    search_fields = ['technology_name']
    view_on_site = False
    empty_value_display = '-empty-'
