# Django imports
from django.contrib import admin
from django.http import HttpResponse

# Local imports
from .models import Employee, Payroll, Skill, Department, Designation

# Third party imports
from reportlab.pdfgen import canvas
from io import BytesIO

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
    list_display = ('employee_id', 'gender', 'marital_status',
                    'job_title', 'date_of_birth', 'phone', 'created_date')
    list_filter = ('employee_id', 'phone')
    search_fields = ['employee_id', 'user_profile__user__first_name', 'user_profile__user__last_name', 'user_profile__user__email', 'phone']
    view_on_site = False
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'account_number', 'gross_salary', 'net_salary')
    list_filter = ('employee__employee_id', 'account_number')
    search_fields = ['employee__user_profile__user__email', 'employee__user_profile__user__first_name', 'employee__user_profile__user__last_name', 'employee__employee_id', 'account_number', 'gross_salary']
    view_on_site = False
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_select_related = ('employee',)
    readonly_fields = ('net_salary',)
    save_as = True
    save_on_top = True
    actions = ['send_payslips']

    def net_salary(self, obj):
        deductions = obj.income_tax + obj.professional_tax + obj.pf_employee + obj.pf_employer + obj.other_charges
        gross_salary = obj.gross_salary
        net_salary = gross_salary - deductions
        return net_salary
    net_salary.short_description = 'Net Salary'

    def send_payslips(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="payslip.pdf"'
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        pdf.drawString(100, 100, "Hello world.")
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        self.message_user(request, "Payslips sent to selected employees successfully.")
        return response
    send_payslips.short_description = "Send payslips to selected users"

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('technology_name',)
    search_fields = ['technology_name']
    view_on_site = False
    empty_value_display = '-empty-'
