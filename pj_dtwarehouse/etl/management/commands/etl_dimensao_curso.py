# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from etl.dao import DAO

from datawarehouse.models import Curso


class Command(BaseCommand):

    def handle(self, *args, **options):

        dao = DAO('postgres')

        #usada para retornar apenas valores distintos
        sql = "SELECT DISTINCT TRIM(ECC.descricao) FROM setor S \
               INNER JOIN  edu_diretoria ED ON ED.setor_id = S.id \
               INNER JOIN  edu_cursocampus ECC ON ECC.diretoria_id = ED.id \
               INNER JOIN  edu_aluno EA ON EA.curso_campus_id = ECC.id \
               INNER JOIN  pessoa_fisica PF ON PF.pessoa_ptr_id = EA.pessoa_fisica_id \
               ORDER BY TRIM(ECC.descricao);"
        bd = dao.get_connection()
        c = bd.cursor()

        c.execute(sql)
        dados = c.fetchall()

        quantidades_criadas = 0
        quantidades_atualizados = 0
        if len(dados) > 0:
            for d in dados:
                curso_nome = d[0]


                # nesta parte é realizada o tratamento dos dados
                curso_nome = curso_nome.title()

                # nesta parte é feita a inserção dos dados na tabela dw
                obj, created = Curso.objects.update_or_create(
                    nome = curso_nome
                )

                if created:
                    quantidades_criadas += 1
                else:
                    quantidades_atualizados += 1

        bd.close()
