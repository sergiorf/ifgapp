# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from models import Tarefa, TipoAtividade, Atividade
from datetime import date

class MetaTarefa():
    def __init__(self, nome, tipo_atividade_pk, atividade_pk, shift):
        self.nome = nome
        self.tipo_atividade_pk = tipo_atividade_pk
        self.atividade_pk = atividade_pk
        self.shift = shift

PRIMEIRA_ANUIDADE = u'1a Anuidade'
ANUIDADE = u'Anuidade'
DESARQUIVAMENTO = u'Desarquivamento: anuidade não paga'
PEDIDO_EXAME = u'Pedido de exame'
DESARQUIVAMENTO_EXAME = u'Desarquivamento: exame não solicitado'
Tarefas = {
    PRIMEIRA_ANUIDADE: MetaTarefa(nome=PRIMEIRA_ANUIDADE, tipo_atividade_pk=2, atividade_pk=7, shift=relativedelta(months=+36)),
    ANUIDADE: MetaTarefa(nome=ANUIDADE, tipo_atividade_pk=2, atividade_pk=7, shift=relativedelta(months=+3)),
    DESARQUIVAMENTO: MetaTarefa(nome=DESARQUIVAMENTO, tipo_atividade_pk=2, atividade_pk=7, shift=relativedelta(months=+3)),
    PEDIDO_EXAME: MetaTarefa(nome=PEDIDO_EXAME, tipo_atividade_pk=1, atividade_pk=4, shift=relativedelta(months=+36)),
    DESARQUIVAMENTO_EXAME: MetaTarefa(nome=DESARQUIVAMENTO_EXAME, tipo_atividade_pk=1, atividade_pk=4, shift=relativedelta(days=+60)),
}


def cria_tarefas(tecnologia):
    if tecnologia.categoria_id == 5:
        cria_tarefas_marca(tecnologia)
    else:
        pass


def cria_tarefas_marca(tecnologia):
    if tecnologia.pedido is not None:
        anuidade = get_last_anuidade(tecnologia)
        if anuidade is None:
            cria_tarefa2(tecnologia, tecnologia.pedido, 1, Tarefas[PRIMEIRA_ANUIDADE])
        elif anuidade.status == Tarefa.FINALIZADA:
            start_dt = date(date.today().year+1, 1, 1)
            cria_tarefa2(tecnologia, start_dt, anuidade.anuidade_nr+1, Tarefas[ANUIDADE])
        elif anuidade.status == Tarefa.NAO_REALIZADA:
            cria_tarefa(tecnologia, anuidade.realizacao_final, Tarefas[DESARQUIVAMENTO])
        tf = get_tarefa(tecnologia, PEDIDO_EXAME)
        if tf is None:
            cria_tarefa(tecnologia, tecnologia.pedido, Tarefas[PEDIDO_EXAME])
        elif tf.status == Tarefa.NAO_REALIZADA:
            cria_tarefa(tecnologia, tf.realizacao_final, Tarefas[DESARQUIVAMENTO_EXAME])


def get_last_anuidade(tecnologia):
    q = Tarefa.objects.filter(tecnologia=tecnologia).filter(nome__contains=ANUIDADE).order_by('realizacao_inicio')
    if len(q) > 0:
        return q[0]
    else:
        return None


def get_tarefa(tecnologia, nome):
    q = Tarefa.objects.filter(tecnologia=tecnologia).filter(nome=nome)
    if len(q) > 0:
        return q[0]
    else:
        return None


def cria_tarefa(tecnologia, start_dt, meta_tarefa):
    return cria_tarefa2(tecnologia, start_dt, 0, meta_tarefa)


def cria_tarefa2(tecnologia, start_dt, anuidade_nr, meta_tarefa):
    tf = Tarefa()
    tf.nome = str(anuidade_nr) + u'a ' + meta_tarefa.nome
    tf.tecnologia = tecnologia
    tf.anuidade_nr = anuidade_nr
    tf.tipo_atividade = TipoAtividade.objects.get(pk=meta_tarefa.tipo_atividade_pk)
    tf.atividade = Atividade.objects.get(pk=meta_tarefa.atividade_pk)
    tf.realizacao_inicio = start_dt
    tf.realizacao_final = start_dt + meta_tarefa.shift
    tf.save()
    return tf
