from django.contrib import admin
from .models import *


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor_planejamento', 'essencial')


class ContaAdmin(admin.ModelAdmin):
    list_display = ('apelido', 'tipo', 'valor')


admin.site.register(Banco)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Conta, ContaAdmin)
