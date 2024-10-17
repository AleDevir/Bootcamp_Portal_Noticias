'''
URLs Aplicação
'''
from django.urls import path

from .views import (
    HomeListView,
    NoticiaDetailView,
    CriarUasuarioView,
)

APP_NAME = "app_noticia"

urlpatterns = [
    path("", HomeListView.as_view(), name='home'),
    path("<int:pk>/", NoticiaDetailView.as_view(), name="noticia-detail"),
    path("register/", CriarUasuarioView.as_view(), name='registrar-usuario'),
]
