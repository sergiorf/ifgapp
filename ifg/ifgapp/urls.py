from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^grupos', 'ifgapp.views.listing_grupos', name='lista_grupos'),
    url(r'^pesquisadores', 'ifgapp.views.listing_pesquisadores', name='lista_pesquisadores'),
    url(r'^servidores', 'ifgapp.views.listing_servidores', name='lista_servidores'),
    url(r'^', 'ifgapp.views.index', name='index'),
)
