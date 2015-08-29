# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import Group, User

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


