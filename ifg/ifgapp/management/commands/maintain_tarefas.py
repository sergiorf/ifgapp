# -*- coding: utf-8 -*-
import datetime
from ifgapp.models import Tarefa
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        today = datetime.datetime.today()
        for t in Tarefa.objects.filter(realizacao_final__lt=today).filter(conclusao__isnull=True):
            t.status = Tarefa.NAO_REALIZADA
            t.clean()
            t.save()