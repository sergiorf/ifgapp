# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Pesquisador, Servidor, Grupo


class ServidorForm(ModelForm):
    class Meta:
        model = Servidor
        exclude = ('user',)


class PesquisadorForm(ModelForm):
    class Meta:
        model = Pesquisador
        exclude = ('user',)


class GrupoForm(ModelForm):
    class Meta:
        model = Grupo
        exclude = ('group',)