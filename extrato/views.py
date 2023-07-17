from datetime import datetime, timedelta
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
        categoria = request.POST.get('categoria-id')
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
                tipo_descricao = 'Entrada'
            else:
                conta.valor -= float(valor)
                tipo_descricao = 'Saída'

            conta.save()
            messages.add_message(request, messages.SUCCESS, f'{tipo_descricao} cadastrada com sucesso.')

        except:
            messages.add_message(request, messages.ERROR, f'Ocorreu um erro ao salvar, tente novamente!')
        
        return redirect(reverse('novo_valor'))
    
    return render(request, 'novo_valor.html', context)


def ver_extrato(request):
    if request.method == 'GET':
        contas = Conta.objects.all().order_by('apelido')
        categorias = Categoria.objects.all().order_by('nome')

        valores = Valores.objects.filter(data__month=datetime.now().month, data__year=datetime.now().year).order_by('-data')

        periodos = {
            '1': 'Somente hoje',
            '7': 'Últimos 7 dias',
            '15': 'Últimos 15 dias',
            '30': 'Últimos 30 dias',
        }

        conta_filter = request.GET.get('conta')
        categoria_filter = request.GET.get('categoria')
        periodo_filter = request.GET.get('periodo')

        if conta_filter:
            valores = valores.filter(conta__id=conta_filter)
            conta_filter = contas.get(id=conta_filter)
            print(f'conta_filter: {conta_filter}')

        if categoria_filter:
            valores = valores.filter(categoria__id=categoria_filter)
            categoria_filter = Categoria.objects.get(id=categoria_filter)

        if periodo_filter == None:
            periodo_filter = '30'

        periodo = [datetime.today() - timedelta(days=int(periodo_filter)), datetime.today()]
        valores = valores.filter(data__range=periodo)

        context = {
            'contas': contas,
            'categorias': categorias,
            'periodos': periodos,
            'valores': valores,
            'conta_filter': conta_filter,
            'categoria_filter': categoria_filter,
            'periodo_filter': periodo_filter
        }

        return render(request, 'ver_extrato.html', context)


def exportar_pdf(request):
    MES_ATUAL = datetime.now().month
    ANO_ATUAL = datetime.now().year
    valores = Valores.objects.filter(data__month=MES_ATUAL, data__year=ANO_ATUAL).order_by('-data')
    contas = Conta.objects.all().order_by('apelido')
    categorias = Categoria.objects.all().order_by('nome')

    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    path_output = BytesIO()

    context = {
        'mes_ano': datetime.now().strftime('%m/%Y'),
        'valores': valores,
        'contas': contas,
        'categorias': categorias,
    }

    template_render = render_to_string(path_template, context)
    HTML(string=template_render).write_pdf(path_output)

    path_output.seek(0)
    
    return FileResponse(path_output, filename="extrato.pdf")