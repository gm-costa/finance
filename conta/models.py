from django.db import models
from perfil.models import Categoria


class ContaPagar(models.Model):
    titulo = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='contas_pagar')
    descricao = models.TextField()
    valor = models.FloatField()
    dia_pagamento = models.IntegerField()
    
    def __str__(self):
        return self.titulo

class ContaPaga(models.Model):
    conta = models.ForeignKey(ContaPagar, on_delete=models.CASCADE, related_name='contas_paga')
    #TODO: como ver se tem a mesma conta vencida em diversos meses ? e quando efetuar o pagamento destas no mesmo dia?
    #data_vencimento = models.DateField()
    data_pagamento = models.DateField()
