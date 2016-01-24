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
TAXA_DECENAL = u'Taxa Decenal'
DESARQUIVAMENTO = u'Desarquivamento: anuidade não paga'
PEDIDO_EXAME = u'Pedido de exame'
DESARQUIVAMENTO_EXAME = u'Desarquivamento: exame não solicitado'
PRIMEIRA_REITERACAO = u'1a reiteração de exigência'
SEGUNDA_REITERACAO = u'2a reiteração de exigência'
ENVIO_DOCS = u'Envio de documentos não obrigatórios do pedido'
Tarefas = {
    PRIMEIRA_ANUIDADE: MetaTarefa(nome=PRIMEIRA_ANUIDADE, tipo_atividade_pk=2, atividade_pk=7, shift=relativedelta(months=+36)),
    ANUIDADE: MetaTarefa(nome=ANUIDADE, tipo_atividade_pk=2, atividade_pk=7, shift=relativedelta(months=+3)),
    TAXA_DECENAL: MetaTarefa(nome=TAXA_DECENAL, tipo_atividade_pk=1, atividade_pk=4, shift=relativedelta(days=+60)),
    DESARQUIVAMENTO: MetaTarefa(nome=DESARQUIVAMENTO, tipo_atividade_pk=2, atividade_pk=7, shift=relativedelta(months=+3)),
    PEDIDO_EXAME: MetaTarefa(nome=PEDIDO_EXAME, tipo_atividade_pk=1, atividade_pk=4, shift=relativedelta(months=+36)),
    DESARQUIVAMENTO_EXAME: MetaTarefa(nome=DESARQUIVAMENTO_EXAME, tipo_atividade_pk=1, atividade_pk=4, shift=relativedelta(days=+60)),
    PRIMEIRA_REITERACAO: MetaTarefa(nome=PRIMEIRA_REITERACAO, tipo_atividade_pk=2, atividade_pk=5, shift=relativedelta(days=+60)),
    SEGUNDA_REITERACAO: MetaTarefa(nome=SEGUNDA_REITERACAO, tipo_atividade_pk=2, atividade_pk=5, shift=relativedelta(days=+60)),
    ENVIO_DOCS: MetaTarefa(nome=ENVIO_DOCS, tipo_atividade_pk=2, atividade_pk=11, shift=relativedelta(days=+60)),
}


def cria_tarefas(tecnologia):
    if tecnologia.categoria_id == 2:
        criar_tarefas_patentes(tecnologia)
    elif tecnologia.categoria.id == 1:
        criar_tarefas_software(tecnologia)
    elif tecnologia.categoria.id == 5:
        criar_tarefas_marcas(tecnologia)
    else:
        criar_tarefas_geral(tecnologia)


def criar_tarefas_geral(tecnologia):
    envio_docs = get_tarefa(tecnologia, ENVIO_DOCS)
    if not envio_docs:
        cria_tarefa(tecnologia, tecnologia.pedido, Tarefas[ENVIO_DOCS])


def criar_tarefas_marcas(tecnologia):
    if tecnologia.pedido is not None:
        taxa_decenal = get_last_by_name(tecnologia, TAXA_DECENAL)
        shift = relativedelta(years=+10)
        if taxa_decenal is None:
            start_dt = tecnologia.pedido + shift
            cria_tarefa2(tecnologia, start_dt, 1, Tarefas[TAXA_DECENAL])
        elif taxa_decenal.status == Tarefa.FINALIZADA:
            start_dt = taxa_decenal.realizacao_inicio + shift
            cria_tarefa2(tecnologia, start_dt, taxa_decenal.numero+1, Tarefas[ANUIDADE])


def criar_tarefas_software(tecnologia):
    ultima_exigencia = get_last_by_atividade(tecnologia, 5)
    if ultima_exigencia and ultima_exigencia.status == Tarefa.NAO_REALIZADA:
        primeira_reiteracao = get_tarefa(tecnologia, PRIMEIRA_REITERACAO)
        if not primeira_reiteracao:
            cria_tarefa(tecnologia, ultima_exigencia.realizacao_final, Tarefas[PRIMEIRA_REITERACAO])
        elif primeira_reiteracao.status == Tarefa.NAO_REALIZADA:
            segunda_reiteracao = get_tarefa(tecnologia, SEGUNDA_REITERACAO)
            if not segunda_reiteracao:
                cria_tarefa(tecnologia, primeira_reiteracao.realizacao_final, Tarefas[SEGUNDA_REITERACAO])


def criar_tarefas_patentes(tecnologia):
    if tecnologia.pedido is not None:
        anuidade = get_last_by_name(tecnologia, ANUIDADE)
        if anuidade is None:
            cria_tarefa2(tecnologia, tecnologia.pedido, 1, Tarefas[PRIMEIRA_ANUIDADE])
        elif anuidade.status == Tarefa.FINALIZADA:
            start_dt = date(date.today().year+1, 1, 1)
            cria_tarefa2(tecnologia, start_dt, anuidade.numero+1, Tarefas[ANUIDADE])
        elif anuidade.status == Tarefa.NAO_REALIZADA:
            cria_tarefa(tecnologia, anuidade.realizacao_final, Tarefas[DESARQUIVAMENTO])
        tf = get_tarefa(tecnologia, PEDIDO_EXAME)
        if tf is None:
            cria_tarefa(tecnologia, tecnologia.pedido, Tarefas[PEDIDO_EXAME])
        elif tf.status == Tarefa.NAO_REALIZADA:
            cria_tarefa(tecnologia, tf.realizacao_final, Tarefas[DESARQUIVAMENTO_EXAME])


def get_last_by_atividade(tecnologia, tipo_atividade_pk):
    tipo_atividade = Atividade.objects.get(pk=tipo_atividade_pk)
    q = Tarefa.objects.filter(tecnologia=tecnologia).filter(atividade=tipo_atividade).order_by('realizacao_inicio')
    if len(q) > 0:
        return q[0]
    else:
        return None


def get_last_by_name(tecnologia, nome):
    q = Tarefa.objects.filter(tecnologia=tecnologia).filter(nome__contains=nome).order_by('realizacao_inicio')
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


def cria_tarefa2(tecnologia, start_dt, numero, meta_tarefa):
    tf = Tarefa()
    if numero > 0:
        tf.nome = str(numero) + u'a ' + meta_tarefa.nome
    else:
        tf.nome = meta_tarefa.nome
    tf.tecnologia = tecnologia
    tf.numero = numero
    tf.tipo_atividade = TipoAtividade.objects.get(pk=meta_tarefa.tipo_atividade_pk)
    tf.atividade = Atividade.objects.get(pk=meta_tarefa.atividade_pk)
    tf.realizacao_inicio = start_dt
    tf.realizacao_final = start_dt + meta_tarefa.shift
    tf.save()
    return tf
