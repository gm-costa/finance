from datetime import datetime
from random import randint
from django.db.models import Sum
from conta.models import ContaPaga, ContaPagar

from extrato.models import Valores


def calcula_total(obj, campo):

    total = obj.aggregate(Sum(campo))[f'{campo}__sum']

    return 0 if total == None else total


def calcula_equilibrio_financeiro():
    gastos_mes_atual = Valores.objects.filter(data__month=datetime.now().month, data__year=datetime.now().year)
    gastos_essenciais = gastos_mes_atual.filter(tipo='S').filter(categoria__essencial=True)
    gastos_nao_essenciais = gastos_mes_atual.filter(tipo='S').filter(categoria__essencial=False)

    total_gastos_essenciais = calcula_total(gastos_essenciais, 'valor')
    total_gastos_nao_essenciais = calcula_total(gastos_nao_essenciais, 'valor')

    return total_gastos_essenciais, total_gastos_nao_essenciais


def percentual_equilibrio_financeiro():
    total_gastos_essenciais, total_gastos_nao_essenciais = calcula_equilibrio_financeiro()
    total = total_gastos_essenciais + total_gastos_nao_essenciais
    try:
        percentual_gastos_essenciais = (total_gastos_essenciais * 100) / total
        percentual_gastos_nao_essenciais = (total_gastos_nao_essenciais * 100) / total

        return round(percentual_gastos_essenciais), round(percentual_gastos_nao_essenciais)
    except:
        return 0, 0


def calcula_percentual_valor(valor, total):
    try:
        percentual_valor = (valor * 100) / total
        return round(percentual_valor)
    
    except:
        return 0


def get_situacao_contas():
    DIA_ATUAL = datetime.now().day
    MES_ATUAL = datetime.now().month
    ANO_ATUAL = datetime.now().year
    
    contas = ContaPagar.objects.all()

    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).filter(data_pagamento__year=ANO_ATUAL).values('conta')

    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
    
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte = DIA_ATUAL + 5).filter(dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)
    
    contas_restantes = contas.exclude(id__in=contas_vencidas).exclude(id__in=contas_pagas).exclude(id__in=contas_proximas_vencimento)

    situacao_contas = {
        'contas_vencidas': contas_vencidas,
        'contas_proximas_vencimento': contas_proximas_vencimento,
        'contas_restantes': contas_restantes,
        'contas_pagas': contas_pagas,
    }

    return situacao_contas


def gera_cor_da_barra():
    cor = 'rgb('
    for i in range(3):
        cor += str(randint(0, 255))
        cor += ',' if i < 2 else ')'

    return cor
