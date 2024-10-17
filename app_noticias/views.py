'''
Módulos views de cadastros
'''

from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.models import User
from django.urls import reverse
from .models import  Noticia
from .forms import RegistrationForm


class HomeListView(ListView):
    '''
    Listar as nóticias na página Home
    '''
    model = Noticia
    template_name = 'home.html'

class NoticiaDetailView(DetailView):
    '''
    Listar as nóticias na página Home
    '''
    model = Noticia
    template_name = 'noticia.html'

class CriarUasuarioView(CreateView):
    '''
    Cria um novo usuário
    '''
    model = User
    template_name = 'register.html'
    form_class = RegistrationForm

    def get_success_url(self):
        return reverse('login')