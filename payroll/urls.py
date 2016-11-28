from django.conf.urls import patterns, include, url

from payroll import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^generate/$', views.generate_payslip, name='generate_payslip'),
]
