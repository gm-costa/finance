from django.contrib import admin
from .models import Planejamento


class PlanejamentoAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'mes_ano', 'valor')


admin.site.register(Planejamento, PlanejamentoAdmin)
