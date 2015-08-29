# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from ifgapp.models import Servidor, AreaConhecimento, Grupo, Permissao
import ifgapp.utils


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'test'
        self.email = 'test@test.com'
        self.password = 'test'
        self.test_user = User.objects.create_user(self.username, self.email, self.password)
        index = 1
        self.grupo_admin = create_obj(dict(nome=u'Admin'), Grupo, dict(
            nome=u'Admin',
        ))
        for perm in Permissao.all_permissions:
            p = sgi.utils.create_obj(dict(codigo=index), Permissao, dict(
                codigo=index,
                descricao=perm
            ))
            index += 1
            self.grupo_admin.permissoes.add(p)
        self.servidor = Servidor(username='test', email='test@test.com',
                            matricula='ABCD1234', grupo=self.grupo_admin)
        self.servidor.save()
        self.areaconhecimento = AreaConhecimento(codigo="1234456", descricao="MATEMATICA")
        self.areaconhecimento.save()

    def assert_no_validation_errors(self, response):
        errors = []
        for line in response.content.split('\n'):
            if line.find('"errorlist"')>0:
                errors.append(line[line.find('<li')+4:line.find('</li')])
        if errors:
            file = open('/tmp/testcase.html', 'w')
            file.write(response.content)
            file.close()
            raise Exception('Erros apresentados no form:\n'+('\n'.join(errors)))
        return True

    def assert_cadastro_object(self, url_cadastro, text, obj_klass, params):
        login = self.client.login(username=self.username, password=self.password)
        self.assertEqual(login, True)
        response = self.client.get(url_cadastro)
        self.assertContains(response, text, status_code=200)
        count = obj_klass.objects.all().count()
        response = self.client.post(url_cadastro, params)
        self.assert_no_validation_errors(response)
        self.assertEquals(obj_klass.objects.all().count(), count+1)

    def assert_list_object(self, url_list):
        login = self.client.login(username=self.username, password=self.password)
        self.assertEqual(login, True)
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, 200)
