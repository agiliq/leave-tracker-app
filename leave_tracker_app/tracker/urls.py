from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('leave_tracker_app.tracker.views', 
    url(r'^$', 'index', name='index'),
    url(r'^apply/$', 'apply', name='apply'),                   
    )
