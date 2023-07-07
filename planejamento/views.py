from django.shortcuts import render
from perfil.models import Categoria

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def definir(request):
    categorias = Categoria.objects.all().order_by('nome')
    return render(request, 'definir_planejamento.html', {'categorias': categorias})


@csrf_exempt
def update_valor_categoria(request, id):
    novo_valor = json.load(request)['novo_valor']
    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejamento = novo_valor
    try:
        categoria.save()
    except:
        return JsonResponse({'status': 'Erro'})

    return JsonResponse({'status': 'Sucesso'})


def ver_planejamento(request):
    categorias = Categoria.objects.all().order_by('nome')
    return render(request, 'ver_planejamento.html', {'categorias': categorias})
