# -*- coding: utf-8 -*-
from ifgapp.tests.test_base import BaseTestCase
from django.core.urlresolvers import reverse
from ifgapp.models import Servidor, Pesquisador


class ServidorTestCase(BaseTestCase):

    def test_cadastro_servidor(self):
        self.assert_cadastro_object(reverse('adicionar_servidor'), 'Adicionar um servidor', Servidor, dict(
                nome = 'qualquer',
                username = u'servidor_test',
                email = 'test@test.com',
                cpf = 2323232323,
                sexo = 'M',
                nome_pai = 'jose',
                nome_mae = 'maria',
                matricula = 'aaaaa',
                grupo=self.grupo_admin.id,
        ))

    def test_list_servidores(self):
        self.assert_list_object(reverse('lista_servidores'))



