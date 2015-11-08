# -*- coding: utf-8 -*-
from django.forms import ModelForm, FileField, Form
from models import Pesquisador, Servidor, Grupo, Tecnologia, Instituicao


class FormPlus(Form):

    """
    Torna o ``request`` disponível no ``FormPlus`` através de ``self.request`` quando passado como parêmetro no inicialização.
    """
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(FormPlus, self).__init__(*args, **kwargs)


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


class TecnologiaForm(ModelForm):
    class Meta:
        model = Tecnologia


class InstituicaoForm(ModelForm):
    class Meta:
        model = Instituicao


class UploadArquivoForm(FormPlus):
    arquivo = FileField()
