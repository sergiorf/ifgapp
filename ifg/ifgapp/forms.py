# -*- coding: utf-8 -*-
from django.forms import ModelForm, FileField, CharField, Form, ChoiceField, ModelChoiceField, DateInput,\
    IntegerField
from models import Pesquisador, Servidor, Grupo, Tecnologia, Instituicao, PessoaFisica, Inventor, Tarefa,\
    Contrato, Categoria, AreaConhecimento, SubAreaConhecimento, Especialidade, UF_CHOICES, TipoAtividade,\
    Atividade
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
    ata_reuniao_comissao_avaliadora = FileField(label='Ata da reunião com Comissão Avaliadora', widget=AdminFileWidget,
                                                max_length=200, required=True)

    class Meta:
        model = Tecnologia
        widgets = {
            'solicitacao_protecao': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'reuniao_com_comissao': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'pedido': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'concessao': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
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
            'realizacao_inicio': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'realizacao_final': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'conclusao': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
        }


class TarefaSearchForm(Form):
    nome = CharField(label=u'Título')
    tipo_atividade = ModelChoiceField(queryset=TipoAtividade.objects.all())
    atividade = ModelChoiceField(queryset=Atividade.objects.all())
    codigo = IntegerField(label=u'Código')
    status = ChoiceField(label=u'Status', choices=(('', '---------'),) + Tarefa.STATUS)


class ContratoForm(autocomplete_light.ModelForm):
    copia_contrato = FileField(label='Cópia do contrato', widget=AdminFileWidget, max_length=200, required=False)

    class Meta:
        model = Contrato
        widgets = {
            'assinatura_acordo': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'vigencia_inicio': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
            'vigencia_fim': DateInput(attrs={'size': '90', 'id': 'datepicker'}),
        }


class ContratoSearchForm(Form):
    codigo = CharField(label=u'Código')
    categoria = ModelChoiceField(queryset=Categoria.objects.all(), required=False)
    tecnologia = ModelChoiceField(queryset=Tecnologia.objects.all())
    modalidade = ChoiceField(label=u'Modalidade contratual', choices=(('', '---------'),) + Contrato.MODALIDADES)


class InstituicaoForm(ModelForm):
    class Meta:
        model = Instituicao


class InstituicaoSearchForm(Form):
    nome = CharField(label=u'Nome')
    sigla = CharField(label=u'Sigla')
    estado = ChoiceField(label=u'Estado', choices=(('', '---------'),) + UF_CHOICES)
    categoria = ChoiceField(label=u'Categoria', choices=(('', '---------'),) + Instituicao.CAT_INSTITUICOES)


class UploadArquivoForm(FormPlus):
    arquivo = FileField()

