'''
Módulos views de cadastros
'''
from django.views.generic import  DetailView, ListView, DeleteView, View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
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
    
class NoticiasView(PermissionRequiredMixin, ListView):
    #Visualiza a área administrativa de notícias
    permission_required = "app_noticias.view_noticia"
    model = Noticia
    template_name = 'noticias_table.html'
    context_object_name = 'noticias'

    def get_queryset(self):
        user = self.request.user
        
        if user.groups.filter(name='Editores').exists():
            return Noticia.objects.all()
        
        elif user.is_authenticated:
            noticias_autor = Noticia.objects.filter(autor=user)
            noticias_publicadas = Noticia.objects.filter(publicada=True).exclude(autor=user)
            return noticias_autor | noticias_publicadas
        return Noticia.objects.filter(publicada=True)

    def get_success_url(self):
        return reverse('home')
    
class CadastrarNoticiaView(PermissionRequiredMixin, CreateView):
    #Cadastra a notícia
    permission_required = "app_noticias.add_noticia"
    model = Noticia
    form_class = NoticiaForm
    template_name = 'noticia_cadastro.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')
    
class EditarNoticiaView(PermissionRequiredMixin, UpdateView):
    #Edita a notícia
    permission_required = "app_noticias.change_noticia"
    model = Noticia
    form_class = NoticiaForm
    template_name = 'noticia_cadastro.html'

    def get_success_url(self):
        return reverse('home')
     
class ExcluirNoticiaView(PermissionRequiredMixin, DeleteView):
    #Exclui a notícia
    permission_required = "app_noticias.delete_noticia"
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


