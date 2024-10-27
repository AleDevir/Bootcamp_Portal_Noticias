'''
Modulo Forms
'''

from django import forms
from django.forms import EmailField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Noticia, Categoria

class RegistrarUsuarioForm(UserCreationForm):
    '''
    Cria um Usuário
    '''
    email = forms.EmailField(required=True)
    class Meta:
        '''
        Metamodelo
        '''
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'subtitulo', 'conteudo', 'imagem', 'categoria', 'fonte_informacao']

class CategoriForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome',  'imagem']
