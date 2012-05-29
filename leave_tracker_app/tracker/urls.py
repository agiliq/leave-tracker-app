from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('tracker.views', 
    url(r'^$', 'index', name='index'),
    )
