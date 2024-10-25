'''
Módulos views de cadastros
'''
from datetime import datetime
from django.core.exceptions import PermissionDenied
from django.views.generic import  DetailView, ListView, DeleteView, View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.forms import BaseModelForm
from django.urls import reverse
from django.shortcuts import (
    HttpResponse,
)
from .models import  Noticia
from .forms import RegistrarUsuarioForm, NoticiaForm




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
        return Noticia.objects.filter(autor=self.request.user)
        
    def get_success_url(self):
        return reverse('noticias')
    
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
        return reverse('noticias')
    
class EditarNoticiaView(PermissionRequiredMixin, UpdateView):
    #Edita a notícia
    permission_required = "app_noticias.change_noticia"
    model = Noticia
    form_class = NoticiaForm
    template_name = 'noticia_cadastro.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        eh_editor: bool = self.request.user.groups.filter(name='Editores').exists()
        if self.object.publicada and not eh_editor:
            raise PermissionDenied('Permissão para alterar a notícia negada! Você não possui permissão necessária.')
        if not eh_editor and self.object.autor != self.request.user:
            raise PermissionDenied('Permissão para alterar a notícia negada! Você não é o autor da notícia.')
        return super().get(request, *args, **kwargs)


    def form_valid(self, form: BaseModelForm) -> HttpResponse: 
        eh_editor: bool = self.request.user.groups.filter(name='Editores').exists()
        if self.object.publicada and not eh_editor:
            raise PermissionDenied('Permissão para alterar a notícia negada! Você não possui permissão necessária.')
        if not eh_editor and self.object.autor != self.request.user:
            raise PermissionDenied('Permissão para alterar a notícia negada! Você não é o autor da notícia.')
        form.instance.atualizada_em = datetime.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('noticias')
     
class ExcluirNoticiaView(PermissionRequiredMixin, DeleteView):
    #Exclui a notícia
    permission_required = "app_noticias.delete_noticia"
    model = Noticia
    template_name = 'noticia_confirm_delete.html'
    context_object_name = 'noticia'

    def form_valid(self, form: BaseModelForm) -> HttpResponse: 
        eh_editor: bool = self.request.user.groups.filter(name='Editores').exists()
        if self.object.publicada and not eh_editor:
            raise PermissionDenied('Permissão para alterar a notícia negada! Você não possui permissão necessária.')
        if not eh_editor and self.object.autor != self.request.user:
            raise PermissionDenied('Permissão para alterar a notícia negada! Você não é o autor da notícia.')
        return super().form_valid(form)

    
    def get_success_url(self):
        return reverse('noticias')
    
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


