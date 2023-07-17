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
        MES_ATUAL = datetime.now().month
        ANO_ATUAL = datetime.now().year

        valores = Valores.objects.filter(categoria__id = self.id).filter(data__month=MES_ATUAL).filter(data__year=ANO_ATUAL)
        valores = valores.filter(tipo='S').aggregate(Sum('valor'))
        
        return valores['valor__sum'] if valores['valor__sum'] else 0

    def calcula_percentual_gasto_por_categoria(self):
        if self.valor_planejamento == 0:
            percentual = 0
        else:
            percentual = (self.total_gasto() * 100) / self.valor_planejamento

        return round(percentual)


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
