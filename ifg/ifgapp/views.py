# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import render, get_object_or_404
from decorators import has_permission
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.template import RequestContext
from models import Permissao, Servidor, Inventor, Grupo, Tecnologia, Tarefa, \
    Instituicao, Arquivo, TecnologiaAnexo, Contrato
from forms import GrupoForm, ServidorForm, InventorForm, TecnologiaForm, TarefaForm, InstituicaoForm, UploadArquivoForm, ContratoForm, TecnologiaSearchForm, InventorSearchForm, InstituicaoSearchForm, TarefaSearchForm, ContratoSearchForm
from django.http import HttpResponse
from utils import to_ascii, get_query
import os


class SearchField(object):
    EXACT_MATCH = 0
    QUERY = 1
    DATE_RANGE = 2


@login_required()
def index(request):
    return render_to_response('index.html', locals())


@login_required()
@has_permission([Permissao.VER_PESSOA])
def listing_servidores(request):
    return __listing_objects(request, Servidor.objects.all(), 'usuario_list.html', "Servidor")


@login_required()
@has_permission([Permissao.VER_PESSOA])
def listing_inventores(request):
    return __listing_objects(request, Inventor.objects.all(), 'usuario_list.html', "Inventor")


@login_required()
@has_permission([Permissao.VER_PESSOA])
def listing_grupos(request):
    return __listing_objects(request, Grupo.objects.all(), 'grupo_list.html', "Grupo")


@login_required()
def listing_tecnologias(request):
    return __listing_objects(request, Tecnologia.objects.order_by('nome').all(), 'tecnologias_list.html', "Tecnologia")


@login_required()
def listing_tarefas(request):
    return __listing_objects(request, Tarefa.objects.all(), 'tarefas_list.html', "Tarefa")


@login_required()
def listing_contratos(request):
    return __listing_objects(request, Contrato.objects.all(), 'contratos_list.html', "Contrato")


@login_required()
def listing_instituicoes(request):
    return __listing_objects(request, Instituicao.objects.all(), 'instituicoes_list.html', "Instituição")


@login_required()
def edit_servidor(request, pk):
    return __edit_object(request, pk, Servidor, 'servidor_edit.html', "lista_servidores")


@login_required()
def edit_inventor(request, pk):
    return __edit_object(request, pk, Inventor, 'inventor_edit.html', "lista_inventores")


@login_required()
def edit_grupo(request, pk):
    return __edit_object(request, pk, Grupo, 'grupo_edit.html', "lista_grupos")


@login_required()
def edit_tecnologia(request, pk):
    return __edit_object(request, pk, Tecnologia, 'tecnologia_edit.html', "lista_tecnologias")


@login_required()
def edit_tarefa(request, pk):
    return __edit_object(request, pk, Tarefa, 'tarefa_edit.html', "lista_tarefas")


@login_required()
def edit_contrato(request, pk):
    return __edit_object(request, pk, Contrato, 'contrato_edit.html', "lista_contratos")


@login_required()
def edit_instituicao(request, pk):
    return __edit_object(request, pk, Instituicao, 'instituicao_edit.html', "lista_instituicoes")


@login_required()
def remover_servidor(request, pk):
    return __remover_object(request, pk, Servidor, 'lista_servidores')


@login_required()
def remover_inventor(request, pk):
    return __remover_object(request, pk, Inventor, 'lista_inventores')


@login_required()
def remover_grupo(request, pk):
    return __remover_object(request, pk, Grupo, 'lista_grupos')


@login_required()
def remover_tecnologia(request, pk):
    return __remover_object(request, pk, Tecnologia, 'lista_tecnologias')


@login_required()
def remover_tarefa(request, pk):
    return __remover_object(request, pk, Tarefa, 'lista_tarefas')


@login_required()
def remover_contrato(request, pk):
    return __remover_object(request, pk, Contrato, 'lista_contratos')


@login_required()
def remover_instituicao(request, pk):
    return __remover_object(request, pk, Instituicao, 'lista_instituicoes')


@login_required()
def adicionar_servidor(request):
    return __adicionar_obj(request, ServidorForm, listing_servidores, 'servidor_add.html')


@login_required()
def adicionar_inventor(request):
    return __adicionar_obj(request, InventorForm, listing_inventores, 'inventor_add.html')


@login_required()
def adicionar_grupo(request):
    return __adicionar_obj(request, GrupoForm, listing_grupos, 'grupo_add.html')


@login_required()
def adicionar_tecnologia(request):
    return __adicionar_obj(request, TecnologiaForm, listing_tecnologias, 'tecnologia_add.html')


@login_required()
def adicionar_tarefa(request):
    return __adicionar_obj(request, TarefaForm, listing_tarefas, 'tarefa_add.html')


@login_required()
def adicionar_contrato(request):
    return __adicionar_obj(request, ContratoForm, listing_contratos, 'contrato_add.html')


@login_required()
def adicionar_instituicao(request):
    return __adicionar_obj(request, InstituicaoForm, listing_instituicoes, 'instituicao_add.html')


@login_required()
def search_tecnologia(request):
    return __search(request, Tecnologia, 'search_tecnologia.html',
                    [('nome', SearchField.QUERY), ('numero_processo', SearchField.QUERY),
                     ('orgao_registro', SearchField.EXACT_MATCH), ('categoria', SearchField.EXACT_MATCH),
                     ('area_conhecimento', SearchField.EXACT_MATCH), ('subarea_conhecimento', SearchField.EXACT_MATCH),
                     ('especialidade', SearchField.EXACT_MATCH), ('criador', SearchField.EXACT_MATCH)],
                    ['solicitacao_protecao', 'reuniao_com_comissao', 'pedido', 'concessao'])


@login_required()
def search_inventor(request):
    return __search(request, Inventor, 'search_inventor.html',
                    [('nome', SearchField.QUERY), ('cpf', SearchField.QUERY),
                     ('instituicao_origem', SearchField.EXACT_MATCH), ('vinculo_ifg', SearchField.EXACT_MATCH)])


@login_required()
def search_instituicao(request):
    return __search(request, Instituicao, 'search_instituicao.html',
                    [('nome', SearchField.QUERY), ('sigla', SearchField.QUERY),
                     ('estado', SearchField.EXACT_MATCH), ('categoria', SearchField.EXACT_MATCH)])


@login_required()
def search_tarefa(request):
    return __search(request, Tarefa, 'search_tarefa.html',
                    [('nome', SearchField.QUERY), ('tipo_atividade', SearchField.EXACT_MATCH),
                     ('atividade', SearchField.EXACT_MATCH), ('codigo', SearchField.QUERY),
                     ('status', SearchField.EXACT_MATCH)],
                    ['realizacao_inicio', 'realizacao_final', 'conclusao'])


@login_required()
def search_contrato(request):
    return __search(request, Contrato, 'search_contrato.html',
                    [('codigo', SearchField.QUERY), ('tecnologia', SearchField.EXACT_MATCH),
                     ('modalidade', SearchField.EXACT_MATCH), ],
                    ['assinatura_acordo', 'vigencia_inicio', 'vigencia_fim'])


@login_required()
def upload_anexo_tecnologia(request, pk):
    return __upload_anexo(request, pk, Tecnologia, TecnologiaAnexo, '/tecnologia/%d/')


@login_required()
def visualizar_arquivo(request, arquivo_id):
    arquivo = Arquivo.objects.all().get(id=arquivo_id)
    arquivo_tmp = arquivo.load()
    if arquivo_tmp is not None:
        response = HttpResponse(arquivo_tmp.read(), content_type=arquivo.content_type())
        response['Content-Disposition'] = 'filename=%s' % \
                to_ascii(arquivo.nome.replace(u'º', '.').replace('/', '-').replace(' ', ''))
        arquivo_tmp.close()
        os.remove(arquivo_tmp.name)
        return response
    else:
        return HttpResponse("O arquivo solicitado foi adulterado ou não existe.")


def login_user(request):
    state = "Por favor autentique-se..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_page = request.POST.get('next')
                if next_page is not None and next_page != 'None':
                    return HttpResponseRedirect(next_page)
                else:
                    return HttpResponseRedirect("/")
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Senha ou nome de usuário incorretos."
    return render_to_response('login.html', {'state': state, 'username': username, 'next': request.GET.get('next')})


def logout_user(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login")


# ------------------------------------------------------------------
# PRIVATE

def __listing_objects(request, queryset, template, klass_name=None):
    return render(request, template, {'objects_tolist': queryset, "klass_name": klass_name})


def __edit_object(request, pk, obj_klass, template_name, list_url):
    obj = get_object_or_404(obj_klass, pk=pk)
    form_klass = obj_klass.__name__ + "Form"
    constructor = globals()[form_klass]
    form = constructor(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse(list_url))
    #Not working with chained selects
    #else:
    #    print form
    #    print form.errors
    aux = []
    if isinstance(obj, Tecnologia):
        aux = TecnologiaAnexo.objects.select_related().filter(tecnologia=obj)
    return render(request, template_name, {'form': form, 'object': obj, 'aux': aux})


def __remover_object(request, pk, obj_klass, list_url):
    obj = get_object_or_404(obj_klass, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return HttpResponseRedirect(reverse(list_url))
    return render(request, 'confirm_delete.html', {'object': obj})


def __adicionar_obj(request, form_klass, listing_fn, template_name):
    context = RequestContext(request)
    if request.method == 'POST':
        form = form_klass(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return listing_fn(request)
        #Not working with chained selects
        #else:
        #    print form
        #    print form.errors
    else:
        form = form_klass()
    return render_to_response(template_name, {'form': form}, context)


@login_required()
def __upload_anexo(request, pk, obj_klass, anexo_klass, url):
    obj = obj_klass.objects.get(pk=pk)
    if request.method == 'POST':
        form = UploadArquivoForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo_up = request.FILES['arquivo']
            nome = arquivo_up.name
            arquivo = Arquivo()
            try:
                arquivo.save(nome)
                anexo = anexo_klass()
                if isinstance(obj, Tecnologia):
                    anexo.tecnologia = obj
                anexo.arquivo = arquivo
                anexo.save()
                arquivo.store(arquivo_up)
                return HttpResponseRedirect(url % obj.id)
            except ValidationError as e:
                form.errors['arquivo'] = '; '.join(e.messages)
    else:
        form = UploadArquivoForm()
    return render(request, 'upload_arquivo.html', {'form': form})


def __search(request, obj_klass, template_name, field_set, range_date_set=[]):
    form_klass = obj_klass.__name__ + "SearchForm"
    constructor_frm = globals()[form_klass]
    if request.method == 'POST':
        results = obj_klass.objects.all()
        if results:
            for field_name, search_type in field_set:
                v = request.POST.get(field_name, None)
                if v:
                    if search_type == SearchField.EXACT_MATCH:
                        results = results.filter(**{field_name: v})
                    elif search_type == SearchField.QUERY:
                        query = get_query(v, [field_name, ])
                        results = results.filter(query)
                    elif search_type == SearchField.DATE_RANGE:
                        pass
                    if not results:
                        break
            if results:
                for field_name in range_date_set:
                    start = request.POST.get(field_name + '_start', None)
                    end = request.POST.get(field_name + '_end', None)
                    if start:
                        results = results.filter(**{field_name+'__gte': start})
                    if end:
                        results = results.filter(**{field_name+'__lte': end})
                    if not results:
                        break
        return render_to_response(template_name, {'form': constructor_frm(request.POST), 'objects_tolist': results})
    else:
        return render_to_response(template_name, {'form': constructor_frm()})