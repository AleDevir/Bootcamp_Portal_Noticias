'''
URLs Aplicação
'''
from django.urls import path
from . import views
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
    
)

APP_NAME = "app_noticia"

urlpatterns = [
    path("", HomeListView.as_view(), name='home'),
    path("register/", CriarUsuarioView.as_view(), name='registrar-usuario'),
    path('register/edit/<int:pk>', UsuarioUpdateView.as_view(), name='atualizar-usuario'),
    path('register/edit/password/<int:pk>', TrocarSenhaView.as_view(), name='atualizar-senha'),
    path('noticias/', NoticiasView.as_view(), name='noticias'),
    path('cadastrar-noticia/', CadastrarNoticiaView.as_view(), name='cadastrar_noticia'),
    path('cadastrar-noticia/<int:pk>/', EditarNoticiaView.as_view(), name='editar_noticia'),
    path('excluir-noticia/<int:pk>/', ExcluirNoticiaView.as_view(), name='excluir_noticia'),
    path('noticias/publicar/<int:noticia_id>/<int:publicado>', views.publicar_noticia, name='publicar-noticia'),
    path("<slug:slug>/", NoticiaDetailView.as_view(), name="noticia-detail"),
]
