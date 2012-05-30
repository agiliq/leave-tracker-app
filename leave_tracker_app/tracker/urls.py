from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('leave_tracker_app.tracker.views', 
    url(r'^$', 'index', name='index'),
    url(r'^apply/$', 'apply', name='apply'),                   
    url(r'^detail/$', 'detail', name='detail'),                   
    url(r'^accounts/login/$', 'aclogin', name='aclogin'),
    url(r'^accounts/logout/$', 'aclogout', name='aclogout'),                       
    )
