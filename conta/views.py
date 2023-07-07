from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from .models import ContaPagar
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
