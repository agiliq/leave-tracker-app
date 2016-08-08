from django.conf.urls import patterns, include, url

from leave_tracker import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^apply/$', views.apply, name='apply'),
    url(r'^all/$', views.all, name='all'),
    url(r'^personal/$', views.personal, name='personal'),
    url(r'^openid/logout/$', views.oidlogout, name='oidlogout'),
    url(r'^get_prev_leaves/', views.get_prev_leaves, name='get_prev_leaves'),
    ]
