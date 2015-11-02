# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import Group, User
from smart_selects.db_fields import ChainedForeignKey
import utils


class Permissao(models.Model):
    VER_TECNOLOGIA = u'Ver Tecnologia'
    VER_PESSOA = u'Ver Pessoa'
    MODIFICAR_TECNOLOGIA = u'Modificar Tecnologia'
    all_permissions = [VER_TECNOLOGIA, VER_PESSOA, MODIFICAR_TECNOLOGIA]
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
    nome = models.CharField(max_length=200)
    email = models.EmailField(blank=True, verbose_name=u'Email principal')

    class Meta:
        ordering = ('nome',)

    def __unicode__(self):
        return u'%s' % self.nome


class PessoaFisica(Pessoa):
    user = models.OneToOneField(User, null=True, blank=True)
    cpf = models.CharField(max_length=20, null=False, verbose_name=u'CPF', blank=True)
    sexo = models.CharField(max_length=1, null=True, choices=[['M', 'Masculino'], ['F', 'Feminino']])
    nome_mae = models.CharField(u'Nome da mãe', max_length=100, null=True)
    nome_pai = models.CharField(u'Nome do pai', max_length=100, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, unique=True)
    grupo = models.ForeignKey(Grupo)

    class Meta:
        verbose_name = u'Pessoa Física'
        verbose_name_plural = u'Pessoas Físicas'

    def save(self, *args, **kwargs):
        """
        Caso `self` tenha username, um usuário será criado para `self`.
        """
        if self.username:
            try:
                user = User.objects.get(username=self.username)
            except User.DoesNotExist:
                user = User.objects.create_user(self.username, email=u'', password='1234')
            self.user = user
        return super(PessoaFisica, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s (%s)' % (self.username, self.cpf)


class Servidor(PessoaFisica):
    matricula = models.CharField(u'Matrícula', max_length=20, unique=True)

    class Meta:
        verbose_name = u'Servidor'
        verbose_name_plural = u'Servidores'

    def __unicode__(self):
        return u'%s (%s)' % (self.username, self.matricula)


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
    INPI = 'INPI'
    FBN = 'FBN'
    EBA = 'EBA'
    ORGAOS_REGISTRO = (
        (INPI, 'INPI'),
        (FBN, 'Fundação Biblioteca Nacional'),
        (EBA, 'Escola de Belas Artes')
    )
    nome = models.CharField(u'Título', max_length=120)
    solicitacao_protecao = models.DateTimeField(u'Data de solicitação da proteção')
    reuniao_com_comissao = models.DateTimeField(u'Data da reunião com Comissão')
    pedido = models.DateTimeField(u'Data do protocolo do pedido')
    protocolo = models.CharField(u'Número de protocolo', max_length=8, default=utils.gen_protocol, unique=True)
    orgao_registro = models.CharField(max_length=4, choices=ORGAOS_REGISTRO, default=INPI)
    area_conhecimento = models.ForeignKey(AreaConhecimento, verbose_name=u'Área do Conhecimento',
                                          related_name=u'area_conhecimento', null=True, blank=True)
    subarea_conhecimento = ChainedForeignKey(SubAreaConhecimento, chained_field='area_conhecimento',
                                             chained_model_field="area", blank=True, null=True)
    especialidade = ChainedForeignKey(Especialidade, chained_field='subarea_conhecimento',
                                      chained_model_field='subarea', blank=True, null=True)
    categoria = models.ForeignKey(Categoria)
    subcategoria = ChainedForeignKey(Subcategoria, chained_field='categoria', chained_model_field="categoria")





