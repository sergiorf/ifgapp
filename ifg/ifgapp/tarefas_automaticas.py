# -*- coding: utf-8 -*-


class MetaTarefa():
    def __init__(self, nome, tipo_atividade_pk, atividade_pk, shift):
        self.nome = nome
        self.tipo_atividade_pk = tipo_atividade_pk
        self.atividade_pk = atividade_pk
        self.shift = shift