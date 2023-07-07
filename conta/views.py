from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from .models import ContaPaga, ContaPagar
from perfil.models import Categoria


def definir_contas(request):
    if request.method == "POST":
        
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')

        if len(titulo.strip()) == 0 or len(categoria.strip()) == 0 or \
                len(descricao.strip()) == 0 or len(valor.strip()) == 0 or \
                len(dia_pagamento.strip()) == 0:
            messages.add_message(request, messages.WARNING, 'Preencha todos os campos!')
            return redirect(reverse('definir_contas'))

        conta = ContaPagar(
            titulo=titulo,
            categoria_id=categoria,
            descricao=descricao,
            valor=valor,
            dia_pagamento=dia_pagamento
        )

        try:
            conta.save()
            messages.add_message(request, messages.SUCCESS, 'Conta cadastrada com sucesso.')
        except:
            messages.add_message(request, messages.ERROR, 'Erro ao salvar, tente novamente!')

        return redirect(reverse('definir_contas'))
    
    else:
        categorias = Categoria.objects.all().order_by('nome')
        return render(request, 'definir_contas.html', {'categorias': categorias})


def ver_contas(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day
    
    contas = ContaPagar.objects.all()

    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')

    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
    
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte = DIA_ATUAL + 5).filter(dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)
    
    contas_restantes = contas.exclude(id__in=contas_vencidas).exclude(id__in=contas_pagas).exclude(id__in=contas_proximas_vencimento)

    context = {
        'contas_vencidas': contas_vencidas,
        'contas_proximas_vencimento': contas_proximas_vencimento,
        'contas_restantes': contas_restantes
    }

    return render(request, 'ver_contas.html', context)
