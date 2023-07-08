from datetime import datetime
from random import randint
from django.db.models import Sum

from extrato.models import Valores


def calcula_total(obj, campo):

    total = obj.aggregate(Sum(campo))[f'{campo}__sum']

    return 0 if total == None else total


def calcula_equilibrio_financeiro():
    gastos_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=True)
    gastos_nao_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=False)

    total_gastos_essenciais = calcula_total(gastos_essenciais, 'valor')
    total_gastos_nao_essenciais = calcula_total(gastos_nao_essenciais, 'valor')

    total = total_gastos_essenciais + total_gastos_nao_essenciais
    try:
        percentual_gastos_essenciais = total_gastos_essenciais * 100 / total
        percentual_gastos_nao_essenciais = total_gastos_nao_essenciais * 100 / total

        return int(percentual_gastos_essenciais), int(percentual_gastos_nao_essenciais)
    
    except:
        return 0, 0


def gera_cor_da_barra():
    cor = 'rgb('
    for i in range(3):
        cor += str(randint(0, 255))
        cor += ',' if i < 2 else ')'

    return cor
