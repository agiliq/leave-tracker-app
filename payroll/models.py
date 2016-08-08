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
    code = models.CharField(name="Designation Code", max_length=10)
    name = models.CharField(name="Job Title", max_length=256)

    def __str__(self):
        return "{0}-{1}".format(self.code, self.name)


class Department(models.Model):
    """
    Stores Employee Department
    """
    code = models.CharField(name="Department Code", max_length=10)
    name = models.CharField(name="Department Name", max_length=256)

    def __str__(self):
        return "{0}-{1}".format(self.code, self.name)


class Skill(models.Model):
    """
    Stores Employee Skills
    """
    technology = models.CharField(name="Technology", max_length=256)

    # def __str__(self):
    #     return self.technology


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
    employee_id = models.CharField(
        name="Employee ID", max_length=20, blank=False)
    gender = models.CharField(
        name="Gender", max_length=2, choices=GENDER_CHOICES, default=MALE)
    date_of_birth = models.DateTimeField(name="Date of Birth", blank=True, null=True)
    marital_status = models.CharField(
        name="Marital Status", max_length=2, choices=STATUS_CHOICES, default=SINGLE)
    address_1 = models.CharField(name="Address 1", max_length=256, blank=True)
    address_2 = models.CharField(name="Address 2", max_length=256, blank=True)
    country = CountryField(name="Country", blank=True)
    zipcode = models.IntegerField(name="Zipcode", blank=True, null=True)
    phone = models.IntegerField(name="Phone", blank=True,  null=True)
    alternate_phone = models.IntegerField(
        name="Alternate Phone", blank=True, null=True)

    # Job Related fields
    department = models.ForeignKey(Department, blank=True, null=True)
    job_title = models.ForeignKey(Designation, blank=True, null=True)
    qualification = models.CharField(max_length=256, name="Qualification", blank=True)
    experience = models.IntegerField(
        name="Experience", blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    resume = models.FileField(upload_to=user_directory_path, blank=True)
    profile_picture = models.ImageField(
        upload_to=user_directory_path, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        try:
            job_title = self.job_title.name
        except AttributeError:
            job_title = ''

        if job_title:
            return "{0} {1} - {2}".format(self.user_profile.user.first_name, self.user_profile.user.last_name, self.job_title.name)
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
    account_number = models.CharField(
        name="Bank Account Number", max_length=256)
    pan_number = models.CharField(name="PAN", max_length=30, blank=True)
    pf_number = models.CharField(
        name="PF Account Number", max_length=50, blank=True)
    gross_salary = models.DecimalField(
        name="Gross Salary", max_digits=6, decimal_places=6)
    basic = models.DecimalField(
        name="Basic Salary", max_digits=6, decimal_places=6)
    hra = models.DecimalField(name="HRA", max_digits=6, decimal_places=6)
    conveyance = models.DecimalField(
        name="Conveyance", max_digits=6, decimal_places=6, blank=True)
    medical = models.DecimalField(
        name="Medical", max_digits=6, decimal_places=6, blank=True)
    flexible_benifits = models.DecimalField(
        name="Flexible Benifits", max_digits=6, decimal_places=6, blank=True)
    pf_employee = models.DecimalField(
        name="PF from Employee", max_digits=6, decimal_places=6, blank=True)
    pf_employer = models.DecimalField(
        name="PF from Employer", max_digits=6, decimal_places=6, blank=True)
    income_tax = models.DecimalField(
        name="Income Tax", max_digits=6, decimal_places=6, blank=True)
    professional_tax = models.DecimalField(
        name="Professional Tax", max_digits=6, decimal_places=6, blank=True)

    def __str__(self):
        return "{0} - {1}".format(self.employee, self.gross_salary)
