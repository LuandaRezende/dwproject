# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from etl.dao import DAO

from datawarehouse.models import Campus


class Command(BaseCommand):

    def handle(self, *args, **options):

        dao = DAO('postgres')

        #usada para retornar apenas valores distintos
        sql = "SELECT DISTINCT TRIM(S.nome) FROM setor S \
               INNER JOIN edu_diretoria ED ON ED.setor_id = S.id \
               INNER JOIN edu_cursocampus ECC ON ECC.diretoria_id = ED.id \
               ORDER BY TRIM(S.nome);"
        bd = dao.get_connection()
        c = bd.cursor()

        c.execute(sql)
        dados = c.fetchall()

        quantidades_criadas = 0
        quantidades_atualizados = 0
        if len(dados) > 0:
            for d in dados:
                campus_nome = d[0]  

                # tratamento dos dados
                campus_nome = campus_nome.replace('CÂMPUS', 'CAMPUS')

                # transformacao e preparacao dos dados para colocar no dw
                campus_nome = campus_nome.title()

                # inserção dos dados na tabela dw
                obj, created = Campus.objects.update_or_create(
                    nome = campus_nome
                )

                if created:
                    quantidades_criadas += 1
                else:
                    quantidades_atualizados += 1

        bd.close()
