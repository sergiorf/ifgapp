# -*- coding: utf-8 -*-
from django.forms import ModelForm, FileField, Form, ModelChoiceField, DateInput
from models import Pesquisador, Servidor, Grupo, Tecnologia, Instituicao, PessoaFisica, Inventor
from django.contrib.admin.widgets import AdminFileWidget


class DateInput(DateInput):
    input_type = 'date'


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


class InventorForm(ModelForm):
    class Meta:
        model = Inventor
        exclude = ('user',)


class GrupoForm(ModelForm):
    class Meta:
        model = Grupo
        exclude = ('group',)


class TecnologiaForm(ModelForm):
    criador = ModelChoiceField(queryset=Inventor.objects.order_by('username'))
    formulario_pedido = FileField(label='Formulário do pedido', widget=AdminFileWidget)
    comprovante_pagamento = FileField(label='Comprovante de pagamento da retribuição (GRU)', widget=AdminFileWidget)
    ata_reuniao_comissao_avaliadora = FileField(label='Ata da reunião com Comissão Avaliadora', widget=AdminFileWidget)
    class Meta:
        model = Tecnologia
        widgets = {
            'solicitacao_protecao': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'reuniao_com_comissao': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'pedido': DateInput(attrs={'size': '90', 'id': 'datepicker'})
        }


class InstituicaoForm(ModelForm):
    class Meta:
        model = Instituicao


class UploadArquivoForm(FormPlus):
    arquivo = FileField()

