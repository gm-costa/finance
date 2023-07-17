from django.db import models
from perfil.models import Categoria


class Planejamento(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='planejamentos')
    mes_ano = models.CharField(max_length=7)
    valor = models.FloatField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['categoria', 'mes_ano'], name='unique_planejamento')
        ]

    def __str__(self) -> str:
        return self.categoria.nome
