# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from ifgapp.models import AreaConhecimento, SubAreaConhecimento, Especialidade, \
    Grupo, Permissao, Servidor, Pesquisador, Inventor, Categoria, Subcategoria, Instituicao, \
    TipoAtividade, Atividade
from ifgapp.utils import create_obj
import string
import os
import re


class Command(BaseCommand):
    def handle(self, *args, **options):
        Command.insert_areacon()
        Command.insert_categorias()
        Command.insert_atividades()
        index = 1
        grupo = create_obj(dict(nome=u'Admin'), Grupo, dict(
            nome=u'Admin',
        ))
        for perm in Permissao.all_permissions:
            p = create_obj(dict(codigo=index), Permissao, dict(
                codigo=index,
                descricao=perm
            ))
            index += 1
            grupo.permissoes.add(p)
        self.create_test_objs(10, grupo)
        create_obj(dict(nome=u'Microsoft'), Instituicao, dict(
            nome=u'Microsoft', sigla='MSFT', endereco='Rua 10', estado='TO', categoria='ICT'
        ))
        create_obj(dict(nome=u'Oracle'), Instituicao, dict(
            nome=u'Oracle', sigla='ORC', endereco='Rua 20', estado='GO', categoria='ICT'
        ))
        create_obj(dict(nome=u'Tesla'), Instituicao, dict(
            nome=u'Tesla', sigla='TES', endereco='Rua 22', estado='SP', categoria='EMP'
        ))

    @staticmethod
    def create_test_objs(nobjs, grupo):
        for index in range(nobjs):
            create_obj(dict(username=u'servidor%s' % index), Servidor, dict(
                username=u'servidor%s' % index,
                email=u'servidor%s@ifg.com.br' % index,
                matricula=u'ABCD1234%s' % index,
                grupo=grupo,
            ))
            create_obj(dict(username=u'pesquisador%s' % index), Pesquisador, dict(
                username=u'pesquisador%s' % index,
                email=u'pesquisador%s@ifg.com.br' % index,
                grupo=grupo,
            ))
            create_obj(dict(username=u'inventor%s' % index), Inventor, dict(
                username=u'inventor%s' % index,
                email=u'inventor%s@ifg.com.br' % index,
                telefone='233-3345',
                vinculoifg=u'02',
                grupo=grupo,
            ))

    @staticmethod
    def parse_treedata(datafile):
        tree = {}
        fname = os.path.join(os.getcwd(), os.path.dirname(__file__)) + '\\' + datafile
        with open(fname, 'r') as f:
            lastline = ''
            for line in f.readlines():
                line = unicode(line, 'utf-8').strip()
                if not line.startswith('#'):
                    tree[line] = []
                    lastline = line
                elif lastline:
                    tree[lastline].append(line[1:].strip())
        return tree

    @staticmethod
    def insert_atividades():
        tree = Command.parse_treedata('atividades.txt')
        for key, value in tree.iteritems():
                c = create_obj(dict(nome=key), TipoAtividade, dict(
                    nome=key,
                ))
                for ativ in value:
                    create_obj(dict(nome=ativ), Atividade, dict(
                        nome=ativ,
                        tipo_atividade=c
                    ))

    @staticmethod
    def insert_categorias():
        tree = Command.parse_treedata('categorias.txt')
        for key, value in tree.iteritems():
            c = create_obj(dict(nome=key), Categoria, dict(
                nome=key,
            ))
            for sub in value:
                create_obj(dict(nome=sub), Subcategoria, dict(
                    nome=sub,
                    categoria=c
                ))

    @staticmethod
    def insert_areacon():
        fname = os.path.join(os.getcwd(), os.path.dirname(__file__)) + '\\areasconhecimento.txt'
        with open(fname, 'r') as f:
            trigers = ['', '', '']
            sups = [None, None]
            for line in f.readlines():
                m = re.match(r"(\d).(\d{2}).(\d{2}).(\d{2})-(\d) (.+)", unicode(line, 'utf-8'))
                codes = []
                for x in range(1, 6):
                    codes.append(m.group(x))
                desc = m.group(6)
                code = string.join(codes, '')
                if codes[0] != trigers[0]:
                    trigers[0] = codes[0]
                    sups[0] = create_obj(dict(codigo=code), AreaConhecimento, dict(
                        codigo=code,
                        descricao=desc,
                    ))
                    #print '%s, %s' % (code, desc)
                elif codes[1] != trigers[1]:
                    trigers[1] = codes[1]
                    sups[1] = create_obj(dict(codigo=code), SubAreaConhecimento, dict(
                        area=sups[0],
                        codigo=code,
                        descricao=desc,
                    ))
                    #print '---%s, %s' % (code, desc)
                elif codes[2] != trigers[2]:
                    trigers[2] = codes[2]
                    create_obj(dict(codigo=code), Especialidade, dict(
                        subarea=sups[1],
                        codigo=code,
                        descricao=desc,
                    ))
                    #print '------%s, %s' % (code, desc)