# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from smart_selects.db_fields import ChainedForeignKey
import utils
import help_text
import error_text
import settings
import os
from datetime import datetime
from utils import mkdir_p
from validators import validate_file_ispdf, validate_telefone
from collections import defaultdict


class Arquivo(models.Model):
    FS_ROOT_PATH = settings.PROJECT_PATH+'/upload/'
    CTYPES = {'pdf': 'application/pdf',
              'txt': 'text/plain',
              'gif': 'image/gif',
              'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
              'tiff': 'image/tiff',
              'png': 'image/png',
              'bmp': 'image/bmp'}
    nome = models.CharField(null=False, unique=False, max_length=255)
    ext = models.CharField(null=False, unique=False, max_length=255)
    data_geracao = models.DateTimeField()

    def __unicode__(self):
        return self.nome

    def content_type(self):
        return Arquivo.CTYPES[self.ext]

    def save(self, nome, *args, **kwargs):
        self.nome = nome
        self.ext = nome.split(".")[-1].lower()
        self.data_geracao = datetime.now()
        errors = defaultdict(list)
        if self.ext not in Arquivo.CTYPES.keys():
            errors['ext'].append(error_text.arquivo_formato_naosuportado)
        if len(errors):
            raise ValidationError(errors)
        super(Arquivo, self).save(*args, **kwargs)

    def store(self, arquivo_upload):
        pathname = self.get_path()[0:self.get_path().rfind('/')]
        mkdir_p(pathname)
        with open(self.get_path(), 'wb+') as arquivo:
            for chunk in arquivo_upload.chunks():
                arquivo.write(chunk)

    def load(self):
        try:
            pathname = self.get_path()
            with open(pathname, 'rb') as arquivo:
                pathname = 'c:\\temp'
                mkdir_p(pathname)
                with open(pathname + '\\temp.%s' % self.ext, 'wb') as temp:
                    temp.write(arquivo.read())
                    return open(temp.name, 'rb')
        except IOError:
            return None

    def delete(self, *args, **kwargs):
        TecnologiaAnexo.objects.filter(arquivo__id=self.id).update(arquivo=None)
        super(Arquivo, self).delete(*args, **kwargs)

    def get_path(self):
        if TecnologiaAnexo.objects.filter(arquivo__id=self.id).exists():
            anexo = TecnologiaAnexo.objects.get(arquivo__id=self.id)
            return Arquivo.FS_ROOT_PATH+'tecnologia/%d/%d.%s' % (anexo.tecnologia_id, anexo.id, self.ext)

UF_CHOICES = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MG', 'Minas Gerais'),
    ('MS', 'Mato Grosso do Sul'),
    ('MT', 'Mato Grosso'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PE', 'Pernanbuco'),
    ('PI', 'Piauí'),
    ('PR', 'Paraná'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('RS', 'Rio Grande do Sul'),
    ('SC', 'Santa Catarina'),
    ('SE', 'Sergipe'),
    ('SP', 'São Paulo'),
    ('TO', 'Tocantins')
)


class Instituicao(models.Model):
    CAT_INSTITUICOES = (
        ('ICT', 'ICT – Instituição de Ciência e Tecnologia'),
        ('EMP', 'Empresa')
    )
    nome = models.CharField(u'Nome', max_length=255, unique=True)
    sigla = models.CharField(u'Sigla', max_length=12, unique=True)
    endereco = models.CharField(u'Endereço', max_length=255)
    telefone = models.CharField(max_length=40)
    estado = models.CharField(u'Estado', max_length=2, choices=UF_CHOICES)
    categoria = models.CharField(u'Categoria', max_length=3, choices=CAT_INSTITUICOES)

    def clean(self):
        errors = defaultdict(list)
        if not validate_telefone(self.telefone):
            errors['telefone'].append(error_text.telefone_error)
        if len(errors):
            raise ValidationError(errors)
        super(Instituicao, self).clean()

    def __unicode__(self):
        return u'%s (%s)' % (self.nome, self.sigla) if self.sigla else u'%s' % self.nome


class Permissao(models.Model):
    VER_TECNOLOGIAS = u'Ver Tecnologias'
    VER_TECNOLOGIAS_PROPRIAS = u'Ver Tecnologias Proprias'
    MODIFICAR_TECNOLOGIAS = u'Modificar Tecnologias'
    VER_PESSOAS = u'Ver Pessoas'
    VER_PESSOAS_MESMO_GRUPO = u'Ver Pessoas do mesmo grupo'
    MODIFICAR_PESSOAS = u'Modificar Pessoas'
    MODIFICAR_PESSOAS_MESMO_GRUPO = u'Modificar Pessoas do mesmo grupo'
    VER_TAREFAS = u'Ver Tarefas'
    MODIFICAR_TAREFAS = u'Modificar Tarefas'
    all_permissions = [VER_TECNOLOGIAS, VER_TECNOLOGIAS_PROPRIAS, MODIFICAR_TECNOLOGIAS,
                       VER_PESSOAS, VER_PESSOAS_MESMO_GRUPO, MODIFICAR_PESSOAS, MODIFICAR_PESSOAS_MESMO_GRUPO,
                       VER_TAREFAS, MODIFICAR_TAREFAS]
    codigo = models.CharField(u'Código', max_length=8, unique=True)
    descricao = models.CharField(u'Descrição', max_length=255)

    def __unicode__(self):
        return u'%s' % self.descricao


class Grupo(models.Model):
    nome = models.CharField(max_length=200)
    group = models.OneToOneField(Group, null=True, blank=True)
    permissoes = models.ManyToManyField(Permissao)

    def save(self, *args, **kwargs):
        try:
            group = Group.objects.get(name=self.nome)
        except Group.DoesNotExist:
            group = Group(name=self.nome)
            group.save()
        self.group = group
        return super(Grupo, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.nome


class Pessoa(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True, verbose_name=u'Email principal')

    class Meta:
        ordering = ('nome',)

    def __unicode__(self):
        return u'%s' % self.nome


class PessoaFisica(Pessoa):
    user = models.OneToOneField(User, null=True, blank=True)
    cpf = models.CharField(max_length=20, null=False, verbose_name=u'CPF', blank=True)
    grupo = models.ForeignKey(Grupo)

    class Meta:
        verbose_name = u'Pessoa Física'
        verbose_name_plural = u'Pessoas Físicas'

    def save(self, *args, **kwargs):
        """
        Caso `self` tenha username, um usuário será criado para `self`.
        """
        if self.nome:
            try:
                user = User.objects.get(username=self.nome)
            except User.DoesNotExist:
                user = User.objects.create_user(self.nome, email=u'', password='1234')
            self.user = user
        return super(PessoaFisica, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s (%s)' % (self.nome, self.cpf) if self.cpf else u'%s' % self.nome


class Servidor(PessoaFisica):
    matricula = models.CharField(u'Matrícula', max_length=20, unique=True)

    class Meta:
        verbose_name = u'Servidor'
        verbose_name_plural = u'Servidores'

    def __unicode__(self):
        return u'%s (%s)' % (self.nome, self.cpf) if self.cpf else u'%s' % self.nome


class Inventor(PessoaFisica):
    VINCULO_IFG = (
        (u'00', u'Aluno'),
        (u'01', u'Professor Efetivo'),
        (u'02', u'Professor Substituto'),
        (u'03', u'Técnico Administrativo'),
        (u'04', u'Estagiário'),
        (u'05', u'Bolsista'),
        (u'06', u'Outro'),
    )
    telefone = models.CharField(max_length=40)
    vinculo_ifg = models.CharField(u'Vínculo IFG', max_length=2, null=True, blank=True, choices=VINCULO_IFG)
    instituicao_origem = models.ForeignKey('ifgapp.Instituicao', verbose_name=u'Instituição de origem', null=True, blank=True)
    doc_comprobatorio = models.FileField(upload_to=utils.doc_location, help_text=help_text.doc_comprobatorio,
                             validators=[validate_file_ispdf], blank=True, null=True, max_length=255)
    docs_pessoais = models.FileField(upload_to=utils.doc_location, help_text=help_text.docs_pessoais,
                             validators=[validate_file_ispdf], blank=True, null=True, max_length=255)

    class Meta:
        verbose_name = u'Inventor'
        verbose_name_plural = u'Inventores'

    def clean(self):
        errors = defaultdict(list)
        if self.vinculo_ifg and self.instituicao_origem:
            errors['vinculo_ifg'].append(error_text.inventor_error_vinculoeinstit)
            errors['instituicao_origem'].append(error_text.inventor_error_vinculoeinstit)
        elif not self.vinculo_ifg and not self.instituicao_origem:
            errors['vinculo_ifg'].append(error_text.inventor_error_semvinculoneminstit)
            errors['instituicao_origem'].append(error_text.inventor_error_semvinculoneminstit)
        if not validate_telefone(self.telefone):
            errors['telefone'].append(error_text.telefone_error)
        if len(errors):
            raise ValidationError(errors)
        super(Inventor, self).clean()

    def __unicode__(self):
        return u'%s (%s)' % (self.nome, self.cpf) if self.cpf else u'%s' % self.nome


class Pesquisador(PessoaFisica):

    class Meta:
        verbose_name = u'Pesquisador'
        verbose_name_plural = u'Pesquisador'


class AreaConhecimento(models.Model):
    codigo = models.CharField(u'Código', max_length=8, unique=True)
    descricao = models.CharField(u'Descrição', max_length=255)

    class Meta:
        verbose_name = u'Área do Conhecimento'
        verbose_name_plural = u'Áreas de Conhecimento'

    def __unicode__(self):
        return u'%s' % self.descricao


class SubAreaConhecimento(models.Model):
    area = models.ForeignKey('ifgapp.AreaConhecimento', null=True, verbose_name=u'Área')
    codigo = models.CharField(u'Código', max_length=8, unique=True)
    descricao = models.CharField(u'Descrição', max_length=255)

    class Meta:
        verbose_name = u'Sub-Área do Conhecimento'
        verbose_name_plural = u'Sub-Áreas de Conhecimento'

    def __unicode__(self):
        return u'%s' % self.descricao


class Especialidade(models.Model):
    subarea = models.ForeignKey('ifgapp.SubAreaConhecimento', null=True, verbose_name=u'Sub-Área')
    codigo = models.CharField(u'Código', max_length=8, unique=True)
    descricao = models.CharField(u'Descrição', max_length=255)

    class Meta:
        verbose_name = u'Especialidade'
        verbose_name_plural = u'Especialidades'

    def __unicode__(self):
        return u'%s' % self.descricao


class Categoria(models.Model):
    nome = models.CharField(u'Nome', max_length=255, unique=True)

    class Meta:
        verbose_name = u'Categoria de Tecnologia'
        verbose_name_plural = u'Categorias de Tecnologia'

    def __unicode__(self):
        return u'%s' % self.nome


class Subcategoria(models.Model):
    categoria = models.ForeignKey('ifgapp.Categoria', null=True, verbose_name=u'Sub-Categoria')
    nome = models.CharField(u'Nome', max_length=255, unique=True)

    class Meta:
        verbose_name = u'Sub-Categoria de Tecnologia'
        verbose_name_plural = u'Sub-Categorias de Tecnologia'

    def __unicode__(self):
        return u'%s' % self.nome


class Tecnologia(models.Model):
    ANCINE = 'ANCINE'
    CONFEA = 'CONFEA'
    INPI = 'INPI'
    EM = 'EM'
    EBA = 'EBA'
    FBN = 'FBN'
    SNPC = 'SNPC'
    ORGAOS_REGISTRO = (
        (ANCINE, 'Agência Nacional de Cinema'),
        (CONFEA, 'Conselho Federal de Engenharia, Arquitetura e Agronomia - CONFEA'),
        (INPI, 'Instituto Nacional da Propriedade Industrial - INPI'),
        (EM, 'Escola de Música da Universidade Federal do Rio de Janeiro - EM'),
        (EBA, 'Escola de Belas Artes - EBA'),
        (FBN, 'Fundação Biblioteca Nacional - FBN'),
        (SNPC, 'Serviço Nacional de Proteção de Cultivares - SNPC')
    )
    STATUS = (
        (u'00', u'Em Exame'),
        (u'01', u'Pedido depositado'),
        (u'03', u'Pedido publicado'),
        (u'04', u'Pedido indeferido'),
        (u'05', u'Pedido deferido'),
        (u'06', u'Prazo para recurso'),
        (u'07', u'Arquivado temporariamente'),
        (u'08', u'Arquivado'),
    )

    class Meta:
        ordering = ('data_cadastro',)


    nome = models.CharField(u'Título', max_length=120, unique=True)
    categoria = models.ForeignKey(Categoria, null=True, blank=True)
    subcategoria = ChainedForeignKey(Subcategoria, chained_field='categoria',
                                     chained_model_field="categoria", null=True, blank=True)
    solicitacao_protecao = models.DateField(u'Data de solicitação da proteção', blank=True, null=True)
    reuniao_com_comissao = models.DateField(u'Data da reunião com Comissão', blank=True, null=True)
    pedido = models.DateField(u'Data do depósito do pedido', blank=True, null=True)
    numero_pedido = models.CharField(u'Número do pedido', max_length=8, default=utils.gen_num_pedido, unique=True)
    numero_protocolo = models.CharField(u'Número do protocolo', max_length=8, default=utils.gen_num_protocolo, unique=True)
    orgao_registro = models.CharField(u'Órgão de registro', max_length=6, choices=ORGAOS_REGISTRO, default=INPI)
    area_conhecimento = models.ForeignKey(AreaConhecimento, verbose_name=u'Área do Conhecimento',
                                          related_name=u'area_conhecimento', null=True, blank=True)
    subarea_conhecimento = ChainedForeignKey(SubAreaConhecimento, chained_field='area_conhecimento',
                                             chained_model_field="area", blank=True, null=True)
    especialidade = ChainedForeignKey(Especialidade, chained_field='subarea_conhecimento',
                                      chained_model_field='subarea', blank=True, null=True)
    cotitulares = models.ManyToManyField('ifgapp.Instituicao', verbose_name=u'Instituições co-titulares',
                                         blank=True, null=True)
    criador = models.ForeignKey(PessoaFisica, verbose_name=u'Criador Responsável', related_name=u'Tecnologia_criador')
    cocriadores = models.ManyToManyField('ifgapp.PessoaFisica', verbose_name=u'Co-criador(es)',
                                         blank=True, null=True, related_name=u'Tecnologia_cocriador')
    observacao = models.TextField(u'Observação', blank=True)
    status = models.CharField(u'Status do pedido', max_length=2, null=True, blank=True, choices=STATUS)
    concessao = models.DateField(u'Data em que o pedido foi concedido', blank=True, null=True)
    formulario_pedido = models.FileField(upload_to=utils.doc_location, validators=[validate_file_ispdf],
                                         max_length=255)
    ata_reuniao_comissao_avaliadora = models.FileField(upload_to=utils.doc_location, validators=[validate_file_ispdf],
                                                       max_length=255)
    data_cadastro = models.DateTimeField(u'Data de cadastro no sistema', default=datetime.now)

    def __unicode__(self):
        return u'%s' % self.nome


class TecnologiaAnexo(models.Model):
    tecnologia = models.ForeignKey(Tecnologia)
    arquivo = models.OneToOneField(Arquivo, null=True)

    def __unicode__(self):
        return self.arquivo.nome


class TipoAtividade(models.Model):
    nome = models.CharField(u'Nome', max_length=255, unique=True)

    class Meta:
        verbose_name = u'Tipo de atividade'
        verbose_name_plural = u'Tipos de atividade'

    def __unicode__(self):
        return u'%s' % self.nome


class Atividade(models.Model):
    tipo_atividade = models.ForeignKey('ifgapp.TipoAtividade', null=True)
    nome = models.CharField(u'Nome', max_length=255, unique=True)

    class Meta:
        verbose_name = u'Atividade'
        verbose_name_plural = u'Atividades'

    def __unicode__(self):
        return u'%s' % self.nome


class Tarefa(models.Model):

    class Meta:
        ordering = ('realizacao_final',)


    AGUARDANDO_INICIO = '00'
    EM_ANDAMENTO = '01'
    FINALIZADA = '02'
    NAO_REALIZADA = '03'
    STATUS = (
        (AGUARDANDO_INICIO, u'Aguardando início'),
        (EM_ANDAMENTO, u'Em andamento'),
        (FINALIZADA, u'Finalizada'),
        (NAO_REALIZADA, u'Não realizada'),
    )
    nome = models.CharField(u'Título', max_length=120, unique=True)
    tecnologia = models.ForeignKey(Tecnologia, verbose_name=u'Tecnologia', related_name=u'Tarefa_tecnologia')
    tipo_atividade = models.ForeignKey(TipoAtividade, null=True, blank=True)
    atividade = ChainedForeignKey(Atividade, chained_field='tipo_atividade',
                                     chained_model_field="tipo_atividade", null=True, blank=True)
    codigo = models.PositiveIntegerField(u'Código', null=True, blank=True)
    numero = models.PositiveIntegerField(u'Numero', null=True, blank=True)
    descricao = models.TextField(u'Descrição', null=True, blank=True)
    realizacao_inicio = models.DateField(u'Data de início da realização da tarefa', blank=True, null=True)
    realizacao_final = models.DateField(u'Data limite para realização da tarefa', blank=True, null=True)
    conclusao = models.DateField(u'Data de conclusão', blank=True, null=True)
    cadastro = models.DateField(u'Data de cadastro', default=datetime.now)
    status = models.CharField(u'Status', max_length=2, null=True, blank=True, choices=STATUS)
    anexo = models.FileField(upload_to=utils.doc_location, help_text=help_text.anexo_tarefa, blank=True, null=True,
                             max_length=255)

    def update_status(self):
        if self.realizacao_inicio:
            if self.cadastro < self.realizacao_inicio:
                self.status = Tarefa.AGUARDANDO_INICIO
            elif self.realizacao_final and self.realizacao_inicio <= self.cadastro < self.realizacao_final:
                self.status = Tarefa.EM_ANDAMENTO

    def validate_errors(self, errors):
        if self.status == Tarefa.FINALIZADA:
            if not self.conclusao:
                errors['conclusao'].append(error_text.data_de_conclusao_error2)
            if not self.anexo:
                errors['anexo'].append(error_text.tarefa_anexo_error)
        elif self.conclusao and self.status != Tarefa.FINALIZADA:
            errors['conclusao'].append(error_text.data_de_conclusao_error)
        if self.realizacao_inicio and not self.realizacao_final:
            errors['realizacao_final'].append(error_text.tarefa_realizacao_final_erro)
        if self.realizacao_final:
            if not self.realizacao_inicio:
                errors['realizacao_inicio'].append(error_text.tarefa_realizacao_inicio_erro)
            if self.cadastro >= self.realizacao_final:
                errors['cadastro'].append(error_text.tarefa_cadastro_erro)

    def clean(self):
        self.update_status()
        errors = defaultdict(list)
        self.validate_errors(errors)
        if len(errors):
            raise ValidationError(errors)
        super(Tarefa, self).clean()


class Contrato(models.Model):
    MODALIDADES = (
        (u'00', u'Assistência técnica e científica'),
        (u'01', u'Convênio'),
        (u'02', u'Contrato de cessão'),
        (u'03', u'Contrato de licença'),
        (u'04', u'Franquia'),
        (u'05', u'Fornecimento de tecnologia (Know-How)'),
        (u'06', u'Protocolo de intenções'),
        (u'07', u'Outro'),
    )
    codigo = models.CharField(max_length=18, default=utils.gen_random(), unique=True)
    modalidade = models.CharField(u'Modalidade contratual', max_length=2, null=True, blank=True, choices=MODALIDADES)
    tecnologia = models.ForeignKey(Tecnologia, verbose_name=u'Tecnologia', related_name=u'Contrato_tecnologia',
                                    null=True, blank=True)
    categoria = models.ForeignKey(Categoria, null=True, blank=True)
    instituicoes_envolvidas = models.ManyToManyField('ifgapp.Instituicao', verbose_name=u'Instituições co-titulares',
                                         blank=True, null=True)
    assinatura_acordo = models.DateField(u'Data de assinatura do acordo', blank=True, null=True)
    vigencia_inicio = models.DateField(u'Data inicio de vigência', blank=True, null=True)
    vigencia_fim = models.DateField(u'Data fim de vigência', blank=True, null=True)
    copia_contrato = models.FileField(u'Cópia do contrato', upload_to=utils.doc_location,
                              help_text=help_text.contrato_fatura, blank=True, null=True, max_length=255)

    def clean(self):
        if self.tecnologia:
            self.categoria = self.tecnologia.categoria
        super(Contrato, self).clean()


#help_text=help_text.observacao,











