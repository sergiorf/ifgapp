# -*- coding: utf-8 -*-
from django.forms import ModelForm, FileField, CharField, Form, ChoiceField, ModelChoiceField, DateInput
from models import Pesquisador, Servidor, Grupo, Tecnologia, Instituicao, PessoaFisica, Inventor, Tarefa,\
    Contrato, Categoria, AreaConhecimento, SubAreaConhecimento, Especialidade
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
    doc_comprobatorio = FileField(label='Documento Comprobatório', widget=AdminFileWidget, max_length=200,
                                  required=False)
    docs_pessoais = FileField(label='Documentos Pessoais', widget=AdminFileWidget, max_length=200, required=False)

    class Meta:
        model = Inventor
        exclude = ('user',)


class InventorSearchForm(Form):
    nome = CharField(label=u'Nome', required=False)
    cpf = CharField(label=u'CPF', required=False)
    instituicao_origem = ModelChoiceField(queryset=Instituicao.objects.all(), required=False)
    vinculo_ifg = ChoiceField(choices=(('', '---------'),) + Inventor.VINCULO_IFG)


class GrupoForm(ModelForm):
    class Meta:
        model = Grupo
        exclude = ('group',)


class TecnologiaForm(autocomplete_light.ModelForm):
    formulario_pedido = FileField(label='Formulário do pedido', widget=AdminFileWidget, max_length=200, required=True)
    comprovante_pagamento = FileField(label='Comprovante de pagamento da retribuição (GRU)', widget=AdminFileWidget,
                                      max_length=200, required=True)
    ata_reuniao_comissao_avaliadora = FileField(label='Ata da reunião com Comissão Avaliadora', widget=AdminFileWidget,
                                                max_length=200, required=True)

    class Meta:
        model = Tecnologia
        widgets = {
            'solicitacao_protecao': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'reuniao_com_comissao': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'pedido': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
        }


class TecnologiaSearchForm(Form):
    nome = CharField(label=u'Título', required=False)
    categoria = ModelChoiceField(queryset=Categoria.objects.all(), required=False)
    numero_processo = CharField(label=u'Número de processo', required=False)
    orgao_registro = ChoiceField(choices=(('', '---------'),) + Tecnologia.ORGAOS_REGISTRO)
    area_conhecimento = ModelChoiceField(queryset=AreaConhecimento.objects.all(), required=False)
    subarea_conhecimento = ModelChoiceField(queryset=SubAreaConhecimento.objects.all(), required=False)
    especialidade = ModelChoiceField(queryset=Especialidade.objects.all(), required=False)
    criador = ModelChoiceField(queryset=Inventor.objects.all(), required=False)
    status = ChoiceField(choices=(('', '---------'),) + Tecnologia.STATUS)


class TarefaForm(autocomplete_light.ModelForm):
    anexo = FileField(label='Anexo', widget=AdminFileWidget, max_length=200, required=False)

    class Meta:
        model = Tarefa
        widgets = {
            'prazo_realizacao_inicio': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'prazo_realizacao_final': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'conclusao': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
        }


class ContratoForm(autocomplete_light.ModelForm):
    formulario = FileField(label='Formulário', widget=AdminFileWidget, max_length=200, required=False)
    carta_explicativa = FileField(label='Carta Explicativa', widget=AdminFileWidget, max_length=200, required=False)
    gru = FileField(label='GRU', widget=AdminFileWidget, max_length=200, required=False)
    fatura = FileField(label='Fatura', widget=AdminFileWidget, max_length=200, required=False)
    ficha_cadastro = FileField(label='Ficha Cadastro', widget=AdminFileWidget, max_length=200, required=False)

    class Meta:
        model = Contrato


class InstituicaoForm(ModelForm):
    class Meta:
        model = Instituicao


class UploadArquivoForm(FormPlus):
    arquivo = FileField()

