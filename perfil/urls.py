from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('gerenciar/', views.gerenciar, name='gerenciar'),
    path('cadastrar_banco/', views.cadastrar_banco, name='cadastrar_banco'),
    path('cadastrar_conta/', views.cadastrar_conta, name='cadastrar_conta'),
    path('excluir_conta/<int:id>/', views.excluir_conta, name="excluir_conta"),
    path('excluir_categoria/<int:id>/', views.excluir_categoria, name="excluir_categoria"),
    path('cadastrar_categoria/', views.cadastrar_categoria, name="cadastrar_categoria"),
    path('alternar_categoria/<int:id>/', views.alternar_categoria, name="alternar_categoria"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('quantidade_contas_categorias/', views.quantidade_contas_categorias, name='quantidade_contas_categorias'),
]
