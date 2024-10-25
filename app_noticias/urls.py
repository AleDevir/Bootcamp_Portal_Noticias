'''
URLs Aplicação
'''
from django.urls import path

from .views import (
    HomeListView,
    NoticiaDetailView,
    CriarUsuarioView,
    TrocarSenhaView,
    UsuarioUpdateView,
    NoticiasView,
    CadastrarNoticiaView, 
    EditarNoticiaView,
    ExcluirNoticiaView,
    PublicarNoticiaView,
    DespublicarNoticiaView,
    
)

APP_NAME = "app_noticia"

urlpatterns = [
    path("", HomeListView.as_view(), name='home'),
    path("<int:pk>/", NoticiaDetailView.as_view(), name="noticia-detail"),
    path("register/", CriarUsuarioView.as_view(), name='registrar-usuario'),
    path('register/edit/<int:pk>', UsuarioUpdateView.as_view(), name='atualizar-usuario'),
    path('register/edit/password/<int:pk>', TrocarSenhaView.as_view(), name='atualizar-senha'),
    path('noticias/<int:pk>', NoticiasView.as_view(), name='noticias'),
    path('cadastrar-noticia/', CadastrarNoticiaView.as_view(), name='cadastrar_noticia'),
    path('cadastrar-noticia/<int:pk>/', EditarNoticiaView.as_view(), name='editar_noticia'),
    path('excluir-noticia/<int:pk>/', ExcluirNoticiaView.as_view(), name='excluir_noticia'),
    path('publicar-noticia/<int:pk>', PublicarNoticiaView.as_view(), name='publicar_noticia'),
    path('despublicar-noticia/<int:pk>/', DespublicarNoticiaView.as_view(), name='despublicar_noticia'),
]
