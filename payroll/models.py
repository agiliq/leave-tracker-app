# Python Imports
from __future__ import unicode_literals

# Django Imports
from django.db import models

# Third party Imports
from django_countries.fields import CountryField

# Local Imports
from leave_tracker.models import UserProfile

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


def user_directory_path(instance, filename):
    return '{0}_{1}/{2}'.format(instance.user.first_name, instance.user.id, filename)


class Designation(models.Model):
    """
    Stores Employee Designation / Job Title
    """
    code = models.CharField("Designation Code", max_length=10)
    title = models.CharField("Job Title", max_length=256)

    def __str__(self):
        return "{0}-{1}".format(self.code, self.name)


class Department(models.Model):
    """
    Stores Employee Department
    """
    code = models.CharField("Department Code", max_length=10)
    name = models.CharField("Department Name", max_length=256)

    def __str__(self):
        return "{0}-{1}".format(self.code, self.name)


class Skill(models.Model):
    """
    Stores Employee Skills
    """
    technology_name = models.CharField(max_length=256)

    def __str__(self):
        return self.technology_name


class Employee(models.Model):
    """
    Stores Employee details
    """
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    MARRIED = 'MR'
    SINGLE = 'S'
    STATUS_CHOICES = (
        ('MR', 'MARRIED'),
        ('S', 'SINGLE'),
    )

    user_profile = models.ForeignKey(UserProfile)
    employee_id = models.CharField(max_length=20, blank=False)
    gender = models.CharField(
        max_length=2, choices=GENDER_CHOICES, default=MALE)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    marital_status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default=SINGLE)
    address_1 = models.CharField(max_length=256, blank=True)
    address_2 = models.CharField(max_length=256, blank=True)
    country = CountryField(blank=True)
    zipcode = models.IntegerField(blank=True, null=True)
    phone = models.IntegerField(blank=True,  null=True)
    alternate_phone = models.IntegerField(blank=True, null=True)

    # Job Related fields
    department = models.ForeignKey(Department, blank=True, null=True)
    job_title = models.ForeignKey(Designation, blank=True, null=True)
    qualification = models.CharField(max_length=256, blank=True)
    experience = models.IntegerField(blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    resume = models.FileField(upload_to=user_directory_path, blank=True)
    profile_picture = models.ImageField(
        upload_to=user_directory_path, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        try:
            job_title = self.job_title.title
        except AttributeError:
            job_title = ''

        if job_title:
            return "{0} {1} - {2}".format(self.user_profile.user.first_name, self.user_profile.user.last_name, self.job_title.title)
        else:
            return "{0} {1}".format(self.user_profile.user.first_name, self.user_profile.user.last_name)

    def get_employee_id(self):
        """
        Returns Employee id directly for now
        """
        return self.employee_id

    def get_date_of_birth(self):
        """
        Return date of birth in human readale format
        """
        return self.date_of_birth.strftime('%d, %b %Y')


class Payroll(models.Model):
    employee = models.ForeignKey(Employee)
    account_number = models.CharField(max_length=256)
    pan_number = models.CharField(max_length=30, blank=True)
    pf_number = models.CharField(
        "PF Account Number", max_length=50, blank=True)
    gross_salary = models.DecimalField(max_digits=6, decimal_places=6)
    basic = models.DecimalField(
        "Basic Salary", max_digits=6, decimal_places=6)
    hra = models.DecimalField("HRA", max_digits=6, decimal_places=6)
    conveyance = models.DecimalField(
        max_digits=6, decimal_places=6, blank=True)
    medical = models.DecimalField(max_digits=6, decimal_places=6, blank=True)
    flexible_benifits = models.DecimalField(
        max_digits=6, decimal_places=6, blank=True)
    pf_employee = models.DecimalField(
        "PF from Employee", max_digits=6, decimal_places=6, blank=True)
    pf_employer = models.DecimalField(
        "PF from Employer", max_digits=6, decimal_places=6, blank=True)
    income_tax = models.DecimalField(
        max_digits=6, decimal_places=6, blank=True)
    professional_tax = models.DecimalField(
        max_digits=6, decimal_places=6, blank=True)

    def __str__(self):
        return "{0} - {1}".format(self.employee, self.gross_salary)
