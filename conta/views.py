from datetime import date, datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse

from perfil.utils import get_situacao_contas
from .models import ContaPaga, ContaPagar
from perfil.models import Categoria, Conta


def definir_contas(request):
    if request.method == "GET":
        categorias = Categoria.objects.all().order_by('nome')
        return render(request, 'definir_contas.html', {'categorias': categorias})
    
    elif request.method == "POST":
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria-id')
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


def ver_contas(request):
    mes_ano = datetime.now().strftime('%Y-%m')
    context = get_situacao_contas()
    context['mes_ano'] = mes_ano

    return render(request, 'ver_contas.html', context)


def pagar_conta(request, id):
    conta = get_object_or_404(ContaPagar, id=id)
    conta_paga = ContaPaga(conta=conta, data_pagamento=date.today())
    try:
        conta_paga.save()
        messages.add_message(request, messages.SUCCESS, 'Conta paga com sucesso.')
    except:
        messages.add_message(request, messages.ERROR, 'Erro ao salvar, tente novamente!')

    return redirect(reverse('ver_contas'))
