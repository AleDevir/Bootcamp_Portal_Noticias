'''
URLs Aplicação
'''
from django.urls import path
from . import views
from .views import (
    HomeListView,
    NoticiaDetailView,
    NoticiaAdmDetailView,
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
    path('', views.root, name='root'),
    path("portal/", HomeListView.as_view(), name='home'),
    path("portal/<slug:slug>/", NoticiaDetailView.as_view(), name="noticia-detail"),
    path("register/", CriarUsuarioView.as_view(), name='registrar-usuario'),
    path('register/edit/<int:pk>', UsuarioUpdateView.as_view(), name='atualizar-usuario'),
    path('register/edit/password/<int:pk>', TrocarSenhaView.as_view(), name='atualizar-senha'),
    path('adm/noticias/', NoticiasView.as_view(), name='noticias'),
    path('adm/noticias/<int:pk>/', NoticiaAdmDetailView.as_view(), name="noticia-adm-detail"),
    path('adm/noticias/cadastro/', CadastrarNoticiaView.as_view(), name='cadastrar_noticia'),
    path('adm/noticias/<int:pk>/cadastro/', EditarNoticiaView.as_view(), name='editar_noticia'),
    path('adm/noticias/<int:pk>/remove/', ExcluirNoticiaView.as_view(), name='excluir_noticia'),
    path('adm/noticias/<int:noticia_id>/publica/<int:publicado>', views.publicar_noticia, name='publicar-noticia'),
]
