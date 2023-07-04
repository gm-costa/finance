from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def __str__(self):
        return self.nome


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
