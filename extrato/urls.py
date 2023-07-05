from django.urls import path
from . import views


urlpatterns = [
    path('novo_valor/', views.novo_valor, name='novo_valor'),
    path('ver_extrato/', views.ver_extrato, name='ver_extrato'),
    path('exportar_pdf/', views.exportar_pdf, name="exportar_pdf"),
]
