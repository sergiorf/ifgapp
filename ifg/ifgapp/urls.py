from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^index/?$', 'ifgapp.views.index', name='index'),
)
