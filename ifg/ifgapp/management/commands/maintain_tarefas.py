# -*- coding: utf-8 -*-
import datetime
from ifgapp.models import Tarefa, Tecnologia
from django.core.management.base import BaseCommand
from ifgapp.tarefas_automaticas import cria_tarefas


class Command(BaseCommand):
    def handle(self, *args, **options):
        today = datetime.datetime.today()
        for t in Tarefa.objects.filter(realizacao_final__lt=today).filter(conclusao__isnull=True):
            t.status = Tarefa.NAO_REALIZADA
            t.clean()
            t.save()
        for tec in Tecnologia.objects.all():
            cria_tarefas(tec)
