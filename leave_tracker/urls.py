from django.conf.urls import patterns, include, url

urlpatterns = patterns('leave_tracker.views',
    url(r'^$', 'index', name='index'),
    url(r'^apply/$', 'apply', name='apply'),
    url(r'^all/$', 'all', name='all'),
    url(r'^personal/$', 'personal', name='personal'),
    url(r'^openid/', include('django_openid_auth.urls')),
    url(r'^openid/logout/$', 'oidlogout', name='oidlogout'),
    url(r'^get_prev_leaves/', 'get_prev_leaves', name='get_prev_leaves'),
    )
