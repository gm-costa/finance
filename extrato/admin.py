from django.contrib import admin
from .models import Valores


class ValoresAdmin(admin.ModelAdmin):
    list_display = ('valor', 'categoria', 'data', 'conta', 'tipo')


admin.site.register(Valores, ValoresAdmin)
