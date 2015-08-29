from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'ifg.views.home', name='home'),
    (r'^accounts/login/$', 'ifgapp.views.login_user'),
    (r'^accounts/logout/$', 'ifgapp.views.logout_user'),
    url(r'^$', include('ifgapp.urls')),
)
