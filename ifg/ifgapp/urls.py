from django.conf.urls import patterns, include, url
import settings
import autocomplete_light

from django.contrib import admin
admin.autodiscover()
autocomplete_light.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/login/$', 'ifgapp.views.login_user', name='login'),
    url(r'^accounts/logout/$', 'ifgapp.views.logout_user', name='logout'),

    url(r'^grupos', 'ifgapp.views.listing_grupos', name='lista_grupos'),
    url(r'^pesquisadores', 'ifgapp.views.listing_pesquisadores', name='lista_pesquisadores'),
    url(r'^servidores', 'ifgapp.views.listing_servidores', name='lista_servidores'),
    url(r'^inventores', 'ifgapp.views.listing_inventores', name='lista_inventores'),
    url(r'^tecnologias', 'ifgapp.views.listing_tecnologias', name='lista_tecnologias'),
    url(r'^instituicoes', 'ifgapp.views.listing_instituicoes', name='lista_instituicoes'),
    url(r'^tarefas', 'ifgapp.views.listing_tarefas', name='lista_tarefas'),
    url(r'^contratos', 'ifgapp.views.listing_contratos', name='lista_contratos'),

    url(r'^servidor/(?P<pk>\d+)/$', 'ifgapp.views.edit_servidor', name='edit_servidor'),
    url(r'^pesquisador/(?P<pk>\d+)/$', 'ifgapp.views.edit_pesquisador', name='edit_pesquisador'),
    url(r'^inventor/(?P<pk>\d+)/$', 'ifgapp.views.edit_inventor', name='edit_inventor'),
    url(r'^grupo/(?P<pk>\d+)/$', 'ifgapp.views.edit_grupo', name='edit_grupo'),
    url(r'^tecnologia/(?P<pk>\d+)/$', 'ifgapp.views.edit_tecnologia', name='edit_tecnologia'),
    url(r'^instituicao/(?P<pk>\d+)/$', 'ifgapp.views.edit_instituicao', name='edit_instituicao'),
    url(r'^tarefa/(?P<pk>\d+)/$', 'ifgapp.views.edit_tarefa', name='edit_tarefa'),
    url(r'^contrato/(?P<pk>\d+)/$', 'ifgapp.views.edit_contrato', name='edit_contrato'),

    url(r'^remover/servidor/(?P<pk>\d+)/$', 'ifgapp.views.remover_servidor', name='remover_servidor'),
    url(r'^remover/pesquisador/(?P<pk>\d+)/$', 'ifgapp.views.remover_pesquisador', name='remover_pesquisador'),
    url(r'^remover/inventor/(?P<pk>\d+)/$', 'ifgapp.views.remover_inventor', name='remover_inventor'),
    url(r'^remover/grupo/(?P<pk>\d+)/$', 'ifgapp.views.remover_grupo', name='remover_grupo'),
    url(r'^remover/tecnologia/(?P<pk>\d+)/$', 'ifgapp.views.remover_tecnologia', name='remover_tecnologia'),
    url(r'^remover/instituicao/(?P<pk>\d+)/$', 'ifgapp.views.remover_instituicao', name='remover_instituicao'),
    url(r'^remover/tarefa/(?P<pk>\d+)/$', 'ifgapp.views.remover_tarefa', name='remover_tarefa'),
    url(r'^remover/contrato/(?P<pk>\d+)/$', 'ifgapp.views.remover_contrato', name='remover_contrato'),

    url(r'^adicionar/servidor', 'ifgapp.views.adicionar_servidor', name='adicionar_servidor'),
    url(r'^adicionar/pesquisador', 'ifgapp.views.adicionar_pesquisador', name='adicionar_pesquisador'),
    url(r'^adicionar/inventor', 'ifgapp.views.adicionar_inventor', name='adicionar_inventor'),
    url(r'^adicionar/grupo', 'ifgapp.views.adicionar_grupo', name='adicionar_grupo'),
    url(r'^adicionar/tecnologia', 'ifgapp.views.adicionar_tecnologia', name='adicionar_tecnologia'),
    url(r'^adicionar/instituicao', 'ifgapp.views.adicionar_instituicao', name='adicionar_instituicao'),
    url(r'^adicionar/tarefa', 'ifgapp.views.adicionar_tarefa', name='adicionar_tarefa'),
    url(r'^adicionar/contrato', 'ifgapp.views.adicionar_contrato', name='adicionar_contrato'),

    url(r'^upload_anexo_tecnologia/(?P<pk>\d+)/$', 'ifgapp.views.upload_anexo_tecnologia', name='upload_anexo_tecnologia'),
    url(r'^visualizar_arquivo/(?P<arquivo_id>\d+)/$', 'ifgapp.views.visualizar_arquivo', name='visualizar_arquivo'),

    url(r'^chaining/', include('smart_selects.urls')),

    url(r'^media/model/documents/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '%s/%s' % (settings.MEDIA_ROOT, settings.MODEL_DOC_ROOT)}),

    url(r"^autocomplete/", include("autocomplete_light.urls")),

    url(r'^$', 'ifgapp.views.index', name='index'),
)
