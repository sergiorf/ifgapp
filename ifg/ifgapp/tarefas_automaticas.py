# -*- coding: utf-8 -*-
from models import Tarefa, Tecnologia
from dateutil.relativedelta import relativedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
import tarefas_automaticas


@receiver(post_save, sender=Tecnologia, dispatch_uid="update_tarefas_automaticas")
def update_tarefas_automaticas(sender, instance, **kwargs):
    tarefas_automaticas.cria_tarefas(instance)


class MetaTarefa():
    nome = ''
    tipo_atividade_pk = -1
    atividade_pk = -1
    shift = None


def cria_tarefas(tecnologia):
    if tecnologia.categoria_id == 5:
        cria_tarefas_marca(tecnologia)
    else:
        pass


def cria_tarefas_marca(tecnologia):
    ANUIDADE = u'1a Anuidade'
    tarefas = {
        ANUIDADE: MetaTarefa(nome=ANUIDADE, tipo_atividade_pk=2, atividade_pk=7, shift=relativedelta(months=+36))
    }
    if tecnologia.pedido is not None:
        tf = Tarefa.objects.get(nome=ANUIDADE)
        if tf is None:
            cria_tarefa(tecnologia, tecnologia.pedido, tarefas[ANUIDADE])


def cria_tarefa(tecnologia, start_dt, meta_tarefa):
    tf = Tarefa()
    tf.nome = meta_tarefa.nome
    tf.tecnologia = tecnologia
    tf.tipo_atividade = meta_tarefa.tipo_atividade_pk
    tf.atividade = meta_tarefa.atividade_pk
    tf.realizacao_inicio = start_dt
    tf.realizacao_final = start_dt + meta_tarefa.shift
    tf.save()

