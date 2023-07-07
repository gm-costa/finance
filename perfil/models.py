from datetime import datetime
from django.db import models
from django.db.models import Sum


class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def __str__(self):
        return self.nome
    
    def total_gasto(self):
        from extrato.models import Valores
        valores = Valores.objects.filter(categoria__id = self.id).filter(data__month=datetime.now().month).aggregate(Sum('valor'))
        return valores['valor__sum'] if valores['valor__sum'] else 0

    def calcula_percentual_gasto_por_categoria(self):
		# Adicione valores no planejamento diferente de 0 para não dar erro
        if self.valor_planejamento == 0:
            percentual = 0
        else:
            percentual = (self.total_gasto() * 100) / self.valor_planejamento

        return int(percentual)


class Banco(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    icone = models.ImageField(upload_to='icones/banco')

    def __str__(self) -> str:
        return self.nome
    

class Conta(models.Model):

    tipo_choices = (
        ('pf', 'Pessoa física'),
        ('pj', 'Pessoa jurídica'),
    )

    apelido = models.CharField(max_length=50, unique=True)
    banco = models.ForeignKey(Banco, on_delete=models.DO_NOTHING, related_name='contas')
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to='icones/conta')

    def __str__(self):
        return self.apelido
