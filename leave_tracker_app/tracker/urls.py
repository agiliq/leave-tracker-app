from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('leave_tracker_app.tracker.views', 
    url(r'^$', 'index', name='index'),
    url(r'^apply/$', 'apply', name='apply'),                   
    url(r'^detail/$', 'detail', name='detail'),                   
    url(r'^personal/$', 'personal', name='personal'),
    url(r'^openid/', include('django_openid_auth.urls')),
    url(r'^openid/logout/$', 'oidlogout', name='oidlogout'),                       
    )
