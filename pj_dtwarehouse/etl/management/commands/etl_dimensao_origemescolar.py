# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from etl.dao import DAO

from datawarehouse.models import OrigemEscolar


class Command(BaseCommand):

    def handle(self, *args, **options):

        dao = DAO('mysql')

        sql = "SELECT DISTINCT TRIM(VA.alternativa) FROM vestibular.alternativas VA \
               WHERE VA.perguntas_idperguntas = 3 \
               ORDER BY TRIM(VA.alternativa);"
        bd = dao.get_connection()
        c = bd.cursor()

        c.execute(sql)
        dados = c.fetchall()
        
        
        quantidades_criados = 0
        quantidades_atualizados = 0
        if len(dados) > 0:
            for d in dados:
                origem_escolar = d[0]


                # inserção dos dados na tabela dw
                obj, created = OrigemEscolar.objects.update_or_create(
                    descricao = origem_escolar
                )

                if created:
                    quantidades_criados += 1
                else:
                    quantidades_atualizados += 1
                    
        bd.close()
