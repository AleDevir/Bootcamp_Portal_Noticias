'''
Módulos views de cadastros
'''

from django.views.generic import ListView
from .models import  Noticia

class HomeListView(ListView):
    '''
    Listar as nóticias na página Home
    '''
    model = Noticia
    template_name = 'home.html'
