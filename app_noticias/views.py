'''
Módulos views de cadastros
'''
from django.views.generic import  DetailView, ListView, DeleteView, View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from .models import  Noticia
from .forms import RegistrarUsuarioForm, NoticiaForm
import pdb


class HomeListView(ListView):
    '''
    Listar as nóticias na página Home
    '''
    model = Noticia
    template_name = 'home.html'

    def get_queryset(self):
        return Noticia.objects.filter(publicada=True)

class NoticiaDetailView(DetailView):
    '''
    Detalhe da Notícia
    '''
    model = Noticia
    template_name = 'noticia.html'

class CriarUsuarioView(CreateView):
    '''
    Cria um novo usuário
    '''
    model = User
    template_name = 'register.html'
    form_class = RegistrarUsuarioForm

    def get_success_url(self):
        return reverse('login')

class UsuarioUpdateView(UpdateView):
    '''
    Atualiza o Usuário
    '''
    model = User
    fields = ['username', 'email']
    template_name = 'user_edit.html'
    def get_success_url(self):
        return reverse('home')

class TrocarSenhaView(PasswordChangeView):
    '''
    Trocar senha
    '''
    form_class = PasswordChangeForm
    template_name = 'password_edit.html'
    def get_success_url(self):
        return reverse('home')
    
class NoticiasView(LoginRequiredMixin, ListView):
    #Visualiza a área administrativa de notícias
    model = Noticia
    template_name = 'noticias_table.html'
    context_object_name = 'noticias'

#"""user.groups.filter(name='Editores').exists"""

    def get_success_url(self):
        return reverse('home')
    
    def get_queryset(self):
        user = self.request.user.groups.filter
        if user(name='Editores').exists():
            return Noticia.objects.all()
        elif user(name='Autores').exists():
            return Noticia.objects.filter()
        return Noticia.objects.none()
    
class CadastrarNoticiaView(LoginRequiredMixin, CreateView):
    #Cadastra a notícia
    model = Noticia
    form_class = NoticiaForm
    template_name = 'noticia_cadastro.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')
    
class EditarNoticiaView(LoginRequiredMixin, UpdateView):
    #Edita a notícia
    model = Noticia
    form_class = NoticiaForm
    template_name = 'noticia_cadastro.html'

    def get_success_url(self):
        return reverse('home')
    
class ExcluirNoticiaView(LoginRequiredMixin, DeleteView):
    #Exclui a notícia
    model = Noticia
    template_name = 'noticia_confirm_delete.html'
    context_object_name = 'noticia'

    def get_success_url(self):
        return reverse('home')
    
class PublicarNoticiaView(LoginRequiredMixin, View):
    def post(self, request, pk):
        noticia = get_object_or_404(Noticia, pk=pk)
        noticia.publicada = True
        noticia.save()
        return redirect('home')


class DespublicarNoticiaView(LoginRequiredMixin, View):
    def post(self, request, pk):
        noticia = get_object_or_404(Noticia, pk=pk)
        noticia.publicada = False
        noticia.save()
        return redirect('home')

