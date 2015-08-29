# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import auth
from models import Permissao, Pesquisador, Servidor, Grupo
from django.shortcuts import render
from decorators import has_permission


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