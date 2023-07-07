from django.urls import path
from . import views


urlpatterns = [
    path('definir/', views.definir, name='definir'),
    path('update_valor_categoria/<int:id>', views.update_valor_categoria, name="update_valor_categoria"),
    path('ver_planejamento/', views.ver_planejamento, name="ver_planejamento")
]
