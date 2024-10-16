'''
URLs Aplicação
'''
from django.urls import path

from .views import HomeListView

APP_NAME = "app_noticia"

urlpatterns = [
    path("", HomeListView.as_view(), name='home')
]
