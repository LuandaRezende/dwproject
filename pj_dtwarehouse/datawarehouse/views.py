from django.shortcuts import render

# Create your views here.

from datawarehouse.models import Aluno

from django.db.models import Count

from django.http import HttpResponse

from io import BytesIO
import base64
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


#foi criado uma função, dps retorna ela e cria o grafico
def index(request):
    alunos_sexo = get_alunos_sexo()
    labels_sexo = []
    values_sexo = []
    for aluno in alunos_sexo:
        labels_sexo.append(aluno['sexo__descricao'])
        values_sexo.append(aluno['total'])

    grafico_sexo = get_pie_graphic(labels_sexo, values_sexo)


    alunos_etnia = get_alunos_etnia()
    labels_etnia = []
    values_etnia = []
    for aluno in alunos_etnia:
        labels_etnia.append(aluno['etnia__descricao'])
        values_etnia.append(aluno['total'])

    grafico_etnia = get_bar_graphic(labels_etnia, values_etnia)

    alunos_origemEscolar = get_alunos_origemEscolar()
    labels_origemEscolar = []
    values_origemEscolar = []
    for aluno in alunos_origemEscolar:
        labels_origemEscolar.append(aluno['origemEscolar__descricao'])
        values_origemEscolar.append(aluno['total'])


    grafico_origemEscolar = get_pie_graphic(labels_origemEscolar, values_origemEscolar)

    alunos_campus = get_alunos_campus()

    alunos_curso = get_alunos_curso()

    context = {'alunos_sexo': alunos_sexo,
               'grafico_sexo': grafico_sexo,
               'alunos_etnia': alunos_etnia,
               'grafico_etnia': grafico_etnia,
               'alunos_origemEscolar': alunos_origemEscolar,
               'grafico_origemEscolar': grafico_origemEscolar,
               'alunos_campus': alunos_campus,
               'alunos_curso': alunos_curso,
            }

    return render(request, 'datawarehouse/index.html', context)


def get_alunos_curso():
    return Aluno.objects.all().values('curso__nome'). \
        annotate(total=Count('*')).order_by('curso__nome')


def get_alunos_campus():
    return Aluno.objects.all().values('campus__nome'). \
        annotate(total=Count('*')).order_by('campus__nome')


def get_alunos_origemEscolar():
    return Aluno.objects.all().values('origemEscolar__descricao'). \
        annotate(total=Count('*')).order_by('origemEscolar__descricao')


def get_alunos_etnia():
    return Aluno.objects.all().values('etnia__descricao'). \
        annotate(total=Count('*')).order_by('etnia__descricao')


def get_alunos_sexo():
    return Aluno.objects.all().values('sexo__descricao'). \
        annotate(total=Count('*')).order_by('sexo__descricao')


def get_pie_graphic(labels, values):
    fig1, ax = plt.subplots(figsize=(10, 4))
    ax.pie(values, labels=labels, autopct='%1.1f%%',
                startangle=90)
    ax.axis('equal')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic


def get_bar_graphic(labels, values):
    x = np.arange(len(labels))  
    width = 0.35 

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, values, width)

    ax.set_ylabel('Quantidade')
    ax.set_title('Quantidade de Alunos por Etnia')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), 
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)

    fig.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic