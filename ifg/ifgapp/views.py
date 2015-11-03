# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import render, get_object_or_404
from decorators import has_permission
from django.core.urlresolvers import reverse
from django.template import RequestContext
from models import Permissao, Pesquisador, Servidor, Grupo, Tecnologia, Instituicao
from forms import GrupoForm, ServidorForm, PesquisadorForm, TecnologiaForm, InstituicaoForm


@login_required()
def index(request):
    return render_to_response('index.html', locals())


@login_required()
@has_permission([Permissao.VER_PESSOA])
def listing_pesquisadores(request):
    return __listing_objects(request, Pesquisador.objects.all(), 'usuario_list.html', "Pesquisador")


@login_required()
@has_permission([Permissao.VER_PESSOA])
def listing_servidores(request):
    return __listing_objects(request, Servidor.objects.all(), 'usuario_list.html', "Servidor")


@login_required()
@has_permission([Permissao.VER_PESSOA])
def listing_grupos(request):
    return __listing_objects(request, Grupo.objects.all(), 'grupo_list.html', "Grupo")


@login_required()
def listing_tecnologias(request):
    return __listing_objects(request, Tecnologia.objects.all(), 'tecnologias_list.html', "Tecnologia")


@login_required()
def listing_instituicoes(request):
    return __listing_objects(request, Instituicao.objects.all(), 'instituicoes_list.html', "Instituição")


@login_required()
def edit_servidor(request, pk):
    return __edit_object(request, pk, Servidor, 'servidor_edit.html', "lista_servidores")


@login_required()
def edit_pesquisador(request, pk):
    return __edit_object(request, pk, Pesquisador, 'pesquisador_edit.html', "lista_pesquisadores")


@login_required()
def edit_grupo(request, pk):
    return __edit_object(request, pk, Grupo, 'grupo_edit.html', "lista_grupos")


@login_required()
def edit_tecnologia(request, pk):
    return __edit_object(request, pk, Tecnologia, 'tecnologia_edit.html', "lista_tecnologias")


@login_required()
def edit_instituicao(request, pk):
    return __edit_object(request, pk, Instituicao, 'instituicao_edit.html', "lista_instituicoes")


@login_required()
def remover_servidor(request, pk):
    return __remover_object(request, pk, Servidor, 'lista_servidores')


@login_required()
def remover_pesquisador(request, pk):
    return __remover_object(request, pk, Pesquisador, 'lista_pesquisadores')


@login_required()
def remover_grupo(request, pk):
    return __remover_object(request, pk, Grupo, 'lista_grupos')


@login_required()
def remover_tecnologia(request, pk):
    return __remover_object(request, pk, Tecnologia, 'lista_tecnologias')


@login_required()
def remover_instituicao(request, pk):
    return __remover_object(request, pk, Instituicao, 'lista_instituicoes')


@login_required()
def adicionar_servidor(request):
    return __adicionar_obj(request, ServidorForm, listing_servidores, 'servidor_add.html')


@login_required()
def adicionar_pesquisador(request):
    return __adicionar_obj(request, PesquisadorForm, listing_servidores, 'pesquisador_add.html')


@login_required()
def adicionar_grupo(request):
    return __adicionar_obj(request, GrupoForm, listing_grupos, 'grupo_add.html')


@login_required()
def adicionar_tecnologia(request):
    return __adicionar_obj(request, TecnologiaForm, listing_tecnologias, 'tecnologia_add.html')


@login_required()
def adicionar_instituicao(request):
    return __adicionar_obj(request, InstituicaoForm, listing_instituicoes, 'instituicao_add.html')


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
    form = constructor(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse(list_url))
    #Not working with chained selects
    #else:
    #    print form
    #    print form.errors
    aux = []
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
        form = form_klass(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return listing_fn(request)
        else:
            print form
            print form.errors
    else:
        form = form_klass()
    return render_to_response(template_name, {'form': form}, context)