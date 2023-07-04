from django.db.models import Sum


def calcula_total(obj, campo):

    total = obj.aggregate(Sum(campo))[f'{campo}__sum']

    return total
