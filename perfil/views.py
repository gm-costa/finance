from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db.models import Sum
from .models import Banco, Categoria, Conta
from .utils import calcula_total


def home(request):
    contas = Conta.objects.all()
    saldo_total = calcula_total(contas, 'valor')
    context = {
        'contas': contas,
        'saldo_total': saldo_total
    }
    return render(request, 'home.html', context)


def gerenciar(request):
    bancos = Banco.objects.all().order_by('nome')
    categorias = Categoria.objects.all().order_by('nome')
    contas = Conta.objects.all().order_by('apelido')

    total_contas = contas.aggregate(Sum('valor'))['valor__sum']

    context = {
        'bancos': bancos,
        'categorias': categorias,
        'contas': contas,
        'total_contas': total_contas,
    }

    return render(request, 'gerenciar.html', context)


def cadastrar_banco(request):
    if request.method == 'POST':
        nome = request.POST.get('nome-banco').strip()
        icone = request.FILES.get('icone-banco')

        # if not icone:
        #     messages.add_message(request, messages.ERROR, "O ícone do banco é obrigatório.")
        #     return redirect(reverse('cadastrar_conta'))

        if len(nome) > 0:
            if Banco.objects.filter(nome=nome).count() > 0:
                messages.add_message(request, messages.ERROR, f"O banco '{nome}' já existe.")
            else:
                banco = Banco(nome=nome, icone=icone)
                try:
                    banco.save()
                    messages.add_message(request, messages.SUCCESS, f"O banco '{nome}' foi cadastrado com sucesso.")
                except:
                    messages.add_message(request, messages.ERROR, 'Ocorreu um erro ao tentar salvar, tente novamente.')
    else:
        messages.add_message(request, messages.ERROR, 'Método inválido.')

    return redirect(reverse('gerenciar'))


def cadastrar_conta(request):
    if request.method == 'POST':
        apelido = request.POST.get('apelido')
        banco = request.POST.get('banco')
        tipo = request.POST.get('tipo')
        valor = request.POST.get('valor')
        icone = request.FILES.get('icone-conta')

        if len(apelido.strip()) == 0 or len(banco.strip()) == 0 or len(tipo.strip()) == 0 or len(valor.strip()) == 0:
            messages.add_message(request, messages.WARNING, 'Todos os campos são obrigatórios, exceto o ícone.')
            return redirect(reverse('gerenciar'))

        if Conta.objects.filter(apelido=apelido).filter(banco_id=banco).exists():
            messages.add_message(request, messages.ERROR, 'Conta já existente.')
        else:       
            conta = Conta(
                apelido=apelido,
                banco_id=banco,
                tipo=tipo,
                valor=valor,
                icone=icone
            )
            try:
                conta.save()
                messages.add_message(request, messages.SUCCESS, 'Conta adicionada com sucesso.')
            except:
                messages.add_message(request, messages.ERROR, 'Ocorreu um erro ao tentar salvar, tente novamente.')

    return redirect(reverse('gerenciar'))


def excluir_conta(request, id):
    if request.method == 'POST':
        conta = get_object_or_404(Conta, id=id)
        try:
            conta.delete()
            messages.add_message(request, messages.SUCCESS, 'Conta removida com sucesso.')
        except:
            messages.add_message(request, messages.ERROR, 'Erro ao tentar excluir, tente novamente.')

    else:
        messages.add_message(request, messages.ERROR, 'Método inválido.')
        
    return redirect(reverse('gerenciar'))


def cadastrar_categoria(request):
    if request.method == 'POST':
        nome = request.POST.get('categoria')
        essencial = bool(request.POST.get('essencial'))

        if len(nome.strip()) == 0:
            messages.add_message(request, messages.WARNING, 'Nome da categoria não informado!')
            return redirect(reverse('gerenciar'))
        
        if Categoria.objects.filter(nome=nome):
            messages.add_message(request, messages.ERROR, 'Categoria já cadastrada!')
            return redirect(reverse('gerenciar'))

        categoria = Categoria(nome=nome, essencial=essencial)
        try:
            categoria.save()
            messages.add_message(request, messages.SUCCESS, 'Categoria cadastrada com sucesso.')
        except:
            messages.add_message(request, messages.ERROR, 'Erro ao tentar salvar a categoria, tente novamente.')

    else:
        messages.add_message(request, messages.ERROR, 'Método inválido.')

    return redirect(reverse('gerenciar'))


def atualizar_categoria(request, id):
    if request.method == 'GET':
        categoria = get_object_or_404(Categoria, id=id)
        categoria.essencial = not categoria.essencial
        try:
            categoria.save()
            messages.add_message(request, messages.SUCCESS, 'Categoria alterada com sucesso.')
        except:
            messages.add_message(request, messages.ERROR, 'Erro ao tentar salvar a categoria, tente novamente.')
    else:
        messages.add_message(request, messages.WARNING, 'Método inválido!')

    return redirect(reverse('gerenciar'))
