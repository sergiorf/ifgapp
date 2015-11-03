from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^accounts/login/$', 'ifgapp.views.login_user', name='login'),
    url(r'^accounts/logout/$', 'ifgapp.views.logout_user', name='logout'),

    url(r'^grupos', 'ifgapp.views.listing_grupos', name='lista_grupos'),
    url(r'^pesquisadores', 'ifgapp.views.listing_pesquisadores', name='lista_pesquisadores'),
    url(r'^servidores', 'ifgapp.views.listing_servidores', name='lista_servidores'),
    url(r'^tecnologias', 'ifgapp.views.listing_tecnologias', name='lista_tecnologias'),
    url(r'^instituicoes', 'ifgapp.views.listing_instituicoes', name='lista_instituicoes'),

    url(r'^servidor/(?P<pk>\d+)/$', 'ifgapp.views.edit_servidor', name='edit_servidor'),
    url(r'^pesquisador/(?P<pk>\d+)/$', 'ifgapp.views.edit_pesquisador', name='edit_pesquisador'),
    url(r'^grupo/(?P<pk>\d+)/$', 'ifgapp.views.edit_grupo', name='edit_grupo'),
    url(r'^tecnologia/(?P<pk>\d+)/$', 'ifgapp.views.edit_tecnologia', name='edit_tecnologia'),
    url(r'^instituicao/(?P<pk>\d+)/$', 'ifgapp.views.edit_instituicao', name='edit_instituicao'),

    url(r'^remover/servidor/(?P<pk>\d+)/$', 'ifgapp.views.remover_servidor', name='remover_servidor'),
    url(r'^remover/pesquisador/(?P<pk>\d+)/$', 'ifgapp.views.remover_pesquisador', name='remover_pesquisador'),
    url(r'^remover/grupo/(?P<pk>\d+)/$', 'ifgapp.views.remover_grupo', name='remover_grupo'),
    url(r'^remover/tecnologia/(?P<pk>\d+)/$', 'ifgapp.views.remover_tecnologia', name='remover_tecnologia'),
    url(r'^remover/instituicao/(?P<pk>\d+)/$', 'ifgapp.views.remover_instituicao', name='remover_instituicao'),

    url(r'^adicionar/servidor', 'ifgapp.views.adicionar_servidor', name='adicionar_servidor'),
    url(r'^adicionar/pesquisador', 'ifgapp.views.adicionar_pesquisador', name='adicionar_pesquisador'),
    url(r'^adicionar/grupo', 'ifgapp.views.adicionar_grupo', name='adicionar_grupo'),
    url(r'^adicionar/tecnologia', 'ifgapp.views.adicionar_tecnologia', name='adicionar_tecnologia'),
    url(r'^adicionar/instituicao', 'ifgapp.views.adicionar_instituicao', name='adicionar_instituicao'),

    url(r'^chaining/', include('smart_selects.urls')),

    url(r'^$', 'ifgapp.views.index', name='index'),
)
