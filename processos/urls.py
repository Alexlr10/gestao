from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import *
from . import views
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [

    path('',views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html',redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # USUARIO
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuario_edit/<int:pk>/', views.usuario_edit, name='usuario_edit'),
    path('usuarios_delete/<pk>',usuariosDelete.as_view(), name='usuarios_delete'),
    path('meus_dados/', views.editar_meus_dados, name='meusdados'),

    # Cliente
    path('cliente/', views.cliente, name='cliente'),
    path('cliente_edit/<int:pk>/', views.cliente_edit, name='cliente_edit'),
    path('cliente_delete/<int:pk>/', views.cliente_delete, name='cliente_delete'),

    # Serviço
    path('servico/', views.servico, name='servico'),
    path('servico_edit/<int:pk>/', views.servico_edit, name='servico_edit'),
    path('servico_delete/<int:pk>/', views.servico_delete, name='servico_delete'),

    # Projeto
    path('projeto/', views.projeto, name='projeto'),
    path('projeto_edit/<int:pk>/', views.projeto_edit, name='projeto_edit'),
    path('projeto_delete/<int:pk>/', views.projeto_delete, name='projeto_delete'),

    # Reuniao
    path('reuniao/', views.reuniao, name='reuniao'),
    path('reuniao_edit/<int:pk>/', views.reuniao_edit, name='reuniao_edit'),
    path('reuniao_delete/<int:pk>/', views.reuniao_delete, name='reuniao_delete'),

    # Ata
    path('ata/', views.ata, name='ata'),
    path('ata_edit/<int:pk>/', views.ata_edit, name='ata_edit'),
    path('ata_delete/<int:pk>/', views.ata_delete, name='ata_delete'),

    # Receita
    path('receita/', views.receita, name='receita'),
    path('receita_edit/<int:pk>/', views.receita_edit, name='receita_edit'),
    path('receita_delete/<int:pk>/', views.receita_delete, name='receita_delete'),

    # Despesas
    path('despesa/', views.despesa, name='despesa'),
    path('despesa_edit/<int:pk>/', views.despesa_edit, name='despesa_edit'),
    path('despesa_delete/<int:pk>/', views.despesa_delete, name='despesa_delete'),


    #Balanco
    path('balanco/', views.balanco, name='balanco'),
    path('balanco_edit/<int:pk>/', views.balanco_edit, name='balanco_edit'),
    path('balanco_delete/<int:pk>/', views.balanco_delete, name='balanco_delete'),

    # Graficos
    path('grafico/', views.grafico, name='grafico'),
    
    path('mensagem/', views.mensagem, name='mensagem'),
    path('ouvidoria/', views.ouvidoria, name='ouvidoria'),
    path('aviso/', views.aviso, name='aviso'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)