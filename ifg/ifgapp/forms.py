# -*- coding: utf-8 -*-
from django.forms import ModelForm, FileField, Form, ModelChoiceField, DateInput
from models import Pesquisador, Servidor, Grupo, Tecnologia, Instituicao, PessoaFisica, Inventor, Tarefa,\
    Contrato
from django.contrib.admin.widgets import AdminFileWidget
import autocomplete_light


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


class InventorForm(autocomplete_light.ModelForm):
    class Meta:
        model = Inventor
        exclude = ('user',)


class GrupoForm(ModelForm):
    class Meta:
        model = Grupo
        exclude = ('group',)


class TecnologiaForm(autocomplete_light.ModelForm):
    formulario_pedido = FileField(label='Formulário do pedido', widget=AdminFileWidget)
    comprovante_pagamento = FileField(label='Comprovante de pagamento da retribuição (GRU)', widget=AdminFileWidget)
    ata_reuniao_comissao_avaliadora = FileField(label='Ata da reunião com Comissão Avaliadora', widget=AdminFileWidget)
    class Meta:
        model = Tecnologia
        widgets = {
            'solicitacao_protecao': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'reuniao_com_comissao': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'pedido': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
        }


class TarefaForm(autocomplete_light.ModelForm):
    class Meta:
        model = Tarefa
        widgets = {
            'prazo_realizacao_inicio': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'prazo_realizacao_final': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'conclusao': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
        }


class ContratoForm(autocomplete_light.ModelForm):
    class Meta:
        model = Contrato


class InstituicaoForm(ModelForm):
    class Meta:
        model = Instituicao


class UploadArquivoForm(FormPlus):
    arquivo = FileField()

