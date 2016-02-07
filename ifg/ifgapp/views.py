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
    Instituicao, Arquivo, TecnologiaAnexo, Contrato, PessoaFisica
from forms import GrupoForm, ServidorForm, InventorForm, TecnologiaForm, \
    TarefaForm, InstituicaoForm, UploadArquivoForm, ContratoForm, TecnologiaSearchForm, \
    InventorSearchForm, InstituicaoSearchForm, TarefaSearchForm, ContratoSearchForm, \
    ServidorVerForm, InventorVerForm, GrupoVerForm, TecnologiaVerForm, InstituicaoVerForm, \
    TarefaVerForm, ContratoVerForm
from django.http import HttpResponse
from utils import to_ascii, get_query, merge_dicts
import os


class SearchField(object):
    EXACT_MATCH = 0
    QUERY = 1
    DATE_RANGE = 2


@login_required()
def index(request):
    return render_to_response('index.html', __perms_dict(request))


@login_required()
def listing_servidores(request):
    servidores = __filter_pessoas(request, Servidor)
    return __listing_objects(request, servidores, 'usuario_list.html', "Servidor")


@login_required()
def listing_inventores(request):
    inventores = __filter_pessoas(request, Inventor)
    return __listing_objects(request, inventores, 'usuario_list.html', "Inventor")


@login_required()
@has_permission([Permissao.VER_PESSOAS])
def listing_grupos(request):
    return __listing_objects(request, Grupo.objects.all(), 'grupo_list.html', "Grupo")


@login_required()
def listing_tecnologias(request):
    perms = __get_permissions(request.user)
    techs = []
    if Permissao.VER_TECNOLOGIAS not in perms and Permissao.VER_TECNOLOGIAS_PROPRIAS in perms:
        try:
            pessoa = PessoaFisica.objects.get(nome=request.user.username)
            techs = Tecnologia.objects.filter(criador=pessoa).order_by('nome').all()
        except PessoaFisica.DoesNotExist:
            pass
    else:
        techs = Tecnologia.objects.order_by('nome').all()
    return __listing_objects(request, techs, 'tecnologias_list.html', "Tecnologia")


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
def ver_servidor(request, pk):
    return __ver_object(request, pk, Servidor, 'servidor_ver.html', "lista_servidores")


@login_required()
def ver_inventor(request, pk):
    return __ver_object(request, pk, Inventor, 'inventor_ver.html', "lista_inventores")


@login_required()
def ver_grupo(request, pk):
    return __ver_object(request, pk, Grupo, 'grupo_ver.html', "lista_grupos")


@login_required()
def ver_tecnologia(request, pk):
    return __ver_object(request, pk, Tecnologia, 'tecnologia_ver.html', "lista_tecnologias")


@login_required()
def ver_instituicao(request, pk):
    return __ver_object(request, pk, Instituicao, 'instituicao_ver.html', "lista_instituicoes")


@login_required()
def ver_tarefa(request, pk):
    return __ver_object(request, pk, Tarefa, 'tarefa_ver.html', "lista_tarefas")


@login_required()
def ver_contrato(request, pk):
    return __ver_object(request, pk, Contrato, 'contrato_ver.html', "lista_contratos")


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
    return __adicionar_obj(request, ServidorForm, 'lista_servidores', 'servidor_add.html')


@login_required()
def adicionar_inventor(request):
    return __adicionar_obj(request, InventorForm, 'lista_inventores', 'inventor_add.html')


@login_required()
def adicionar_grupo(request):
    return __adicionar_obj(request, GrupoForm, 'lista_grupos', 'grupo_add.html')


@login_required()
def adicionar_tecnologia(request):
    return __adicionar_obj(request, TecnologiaForm, 'lista_tecnologias', 'tecnologia_add.html')


@login_required()
def adicionar_tarefa(request):
    return __adicionar_obj(request, TarefaForm, 'lista_tarefas', 'tarefa_add.html')


@login_required()
def adicionar_contrato(request):
    return __adicionar_obj(request, ContratoForm, 'lista_contratos', 'contrato_add.html')


@login_required()
def adicionar_instituicao(request):
    return __adicionar_obj(request, InstituicaoForm, 'lista_instituicoes', 'instituicao_add.html')


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
    error = None
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
                error = "Your account is not active, please contact the site admin."
        else:
            error = "Senha ou nome de usuário incorretos."
    return render_to_response('login.html', {'state': state, 'error': error, 'username': username, 'next': request.GET.get('next')})


def logout_user(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login")


# ------------------------------------------------------------------
# PRIVATE

def __listing_objects(request, queryset, template, klass_name=None):
    x = {'objects_tolist': queryset, "klass_name": klass_name}
    perms = __perms_dict(request)
    return render(request, template, merge_dicts(x, perms))


def __ver_object(request, pk, obj_klass, template_name, list_url):
    obj = get_object_or_404(obj_klass, pk=pk)
    form_klass = obj_klass.__name__ + "VerForm"
    constructor = globals()[form_klass]
    form = constructor(request.POST or None, request.FILES or None, instance=obj)
    aux = []
    if isinstance(obj, Tecnologia):
        aux = TecnologiaAnexo.objects.select_related().filter(tecnologia=obj)
    x = {'form': form, 'object': obj, 'aux': aux}
    perms = __perms_dict(request)
    return render(request, template_name, merge_dicts(x, perms))


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
    x = {'form': form, 'object': obj, 'aux': aux}
    perms = __perms_dict(request)
    return render(request, template_name, merge_dicts(x, perms))


def __remover_object(request, pk, obj_klass, list_url):
    obj = get_object_or_404(obj_klass, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return HttpResponseRedirect(reverse(list_url))
    return render(request, 'confirm_delete.html', {'object': obj})


def __adicionar_obj(request, form_klass, list_url, template_name):
    context = RequestContext(request)
    if request.method == 'POST':
        form = form_klass(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse(list_url))
        #Not working with chained selects
        #else:
        #    print form
        #    print form.errors
    else:
        form = form_klass()
    x = {'form': form}
    perms = __perms_dict(request)
    return render_to_response(template_name, merge_dicts(x, perms), context)


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
        nothing_exists = True
        results = obj_klass.objects.all()
        if results:
            nothing_exists = False
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
        return render_to_response(template_name, {'form': constructor_frm(request.POST), 'nothing_exists': nothing_exists, 'method': request.method, 'objects_tolist': results})
    else:
        return render_to_response(template_name, {'form': constructor_frm()})


def __get_permissions(user):
    if user.is_superuser:
        return Permissao.all_permissions
    else:
        try:
            pessoa = PessoaFisica.objects.get(nome=user.username)
            return list(pessoa.grupo.permissoes.values_list('descricao', flat=True))
        except Inventor.DoesNotExist:
            return []


def __perms_dict(request):
    perms = __get_permissions(request.user)
    return dict({'perms': perms,
        'ver_techs': Permissao.VER_TECNOLOGIAS, 'ver_techs_proprias': Permissao.VER_TECNOLOGIAS_PROPRIAS,
        'mod_techs': Permissao.MODIFICAR_TECNOLOGIAS, 'ver_pessoas': Permissao.VER_PESSOAS,
        'ver_pessoas_mesmo_grupo': Permissao.VER_PESSOAS_MESMO_GRUPO, 'mod_pessoas': Permissao.MODIFICAR_PESSOAS,
        'ver_tarefas': Permissao.VER_TAREFAS, 'mod_tarefas': Permissao.MODIFICAR_TAREFAS
    })


def __filter_pessoas(request, userklass):
    perms = __get_permissions(request.user)
    pessoas = []
    if Permissao.VER_PESSOAS not in perms and Permissao.VER_PESSOAS_MESMO_GRUPO in perms:
        try:
            pessoa = PessoaFisica.objects.get(nome=request.user.username)
            pessoas = userklass.objects.filter(grupo=pessoa.grupo).order_by('nome').all()
        except PessoaFisica.DoesNotExist:
            pass
    else:
        pessoas = userklass.objects.all()
    return pessoas