from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from social.apps import django_app

urlpatterns = [
    # Examples:
    url(r'', include('leave_tracker.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url('google_auth/', include('social.apps.django_app.urls', namespace='social')),
    url('google_auth/login/google-oauth2/', django_app.views.auth, name='login'),
]

urlpatterns += staticfiles_urlpatterns()
