from datetime import datetime
from django.shortcuts import render
from extrato.models import Valores
from perfil.models import Categoria
from perfil.utils import calcula_total, calcula_percentual_valor
from planejamento.models import Planejamento

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json


def definir_planejamento(request):
    mes_ano = datetime.now().strftime('%Y-%m')
    valores_entradas = Valores.objects.filter(tipo='E').values('categoria')
    categorias = Categoria.objects.exclude(id__in=valores_entradas).order_by('nome')
    return render(request, 'definir_planejamento.html', {'categorias': categorias, 'mes_ano': mes_ano})


@csrf_exempt
def update_valor_categoria(request, id):
    novo_valor = json.load(request)['novo_valor']
    novo_valor = float(novo_valor.replace('.', '').replace(',', '.'))

    if not isinstance(novo_valor, float):
        messages.add_message(request, messages.ERROR, f"O valor informado para a categoria '{categoria}' não é válido!")
        return JsonResponse({'status': 'Erro'})

    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejamento = novo_valor

    try:
        categoria.save()
        messages.add_message(request, messages.SUCCESS, f"Valor planejamento de '{categoria}' cadastrado com sucesso.")
        return JsonResponse({'status': 'Sucesso'})
    except:
        messages.add_message(request, messages.ERROR, 'Erro ao salvar, tente novamente!')
        return JsonResponse({'status': 'Erro'})


def ver_planejamento(request):
    mes_ano = datetime.now().strftime('%Y-%m')
    valores_entradas = Valores.objects.filter(tipo='E').values('categoria')
    categorias = Categoria.objects.exclude(id__in=valores_entradas).order_by('nome')

    total_valor_gasto = 0
    for categoria in categorias:
        total_valor_gasto += categoria.total_gasto()

    total_valor_planejamento = calcula_total(categorias, 'valor_planejamento')

    total_percentual_gasto = calcula_percentual_valor(total_valor_gasto, total_valor_planejamento)

    context = {
        'mes_ano': mes_ano,
        'categorias': categorias,
        'total_valor_gasto': total_valor_gasto,
        'total_valor_planejamento': total_valor_planejamento,
        'total_percentual_gasto': total_percentual_gasto,
    }

    return render(request, 'ver_planejamento.html', context)
