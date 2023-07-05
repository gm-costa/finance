from datetime import datetime
from io import BytesIO
import os
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
from weasyprint import HTML
from perfil.models import Conta, Categoria
from .models import Valores


def novo_valor(request):
    contas = Conta.objects.all().order_by('apelido')
    categorias = Categoria.objects.all() .order_by('nome')
    context = {
        'contas': contas,
        'categorias': categorias
    }

    if request.method == "POST":
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')

        if len(valor.strip()) == 0  or len(categoria.strip()) == 0 \
                or len(descricao.strip()) == 0 or len(data.strip()) == 0 \
                or len(conta.strip()) == 0 or len(tipo.strip()) == 0:
            messages.add_message(request, messages.WARNING, 'Preencha todos os campos!')
            return redirect(reverse('novo_valor'))
        
        valores = Valores(
            valor=valor,
            categoria_id=categoria,
            descricao=descricao,
            data=data,
            conta_id=conta,
            tipo=tipo,
        )

        try:
            valores.save()

            conta = Conta.objects.get(id=conta)

            if tipo == 'E':
                conta.valor += float(valor)
            else:
                conta.valor -= float(valor)

            conta.save()
            messages.add_message(request, messages.SUCCESS, 'Categoria cadastrada com sucesso')
        except Exception as e:
            messages.add_message(request, messages.ERROR, f'Ocorreu um erro ao salvar, tente novamente!\n{e}')
        
        return redirect(reverse('novo_valor'))
    
    return render(request, 'novo_valor.html', context)


def ver_extrato(request):
    contas = Conta.objects.all().order_by('apelido')
    categorias = Categoria.objects.all().order_by('nome')

    valores = Valores.objects.filter(data__month=datetime.now().month)

    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')

    if conta_get:
        valores = valores.filter(conta__id=conta_get)
    if categoria_get:
        valores = valores.filter(categoria__id=categoria_get)

    context = {
        'valores': valores,
        'contas': contas,
        'categorias': categorias
    }

    return render(request, 'ver_extrato.html', context)


def exportar_pdf(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    contas = Conta.objects.all().order_by('apelido')
    categorias = Categoria.objects.all().order_by('nome')
    
    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    path_output = BytesIO()

    context = {
        'valores': valores,
        'contas': contas,
        'categorias': categorias
    }

    template_render = render_to_string(path_template, context)
    HTML(string=template_render).write_pdf(path_output)

    path_output.seek(0)
    
    return FileResponse(path_output, filename="extrato.pdf")