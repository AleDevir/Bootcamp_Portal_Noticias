'''
Módulos views de cadastros
'''
from datetime import datetime
from django.template.defaultfilters import slugify
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import  DetailView, ListView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.forms import BaseModelForm
from django.urls import reverse
from django.shortcuts import (
    render,
    HttpResponse,
    HttpResponseRedirect,
)
from .models import  Noticia, Categoria
from .forms import RegistrarUsuarioForm, NoticiaForm, CategoriaForm

def root(request) -> HttpResponse:
    '''
    Redirecionamento de root para home
    '''
    return HttpResponseRedirect(reverse("home"))

class NoticiasBaseListView(ListView):
    '''
    Classe base da listagem das notícias (home e área administrativa)
    '''
    model = Noticia
    context_object_name = 'noticias'
    titulo_pesquisado = ''
    categoria_pesquisada = 0
    publicada = False

    def get(self, request, *args, **kwargs):
        categoria_querystring = self.request.GET.get('categoria', 0)
        if categoria_querystring:
            self.categoria_pesquisada = int(categoria_querystring)
        return render(request, self.template_name, {
            'titulo_pesquisado': self.titulo_pesquisado,
            'categoria_pesquisada': self.categoria_pesquisada,
            'categorias': Categoria.objects.all(),
            'noticias': self.get_queryset(),
        })

    def post(self, request, *args, **kwargs):
        self.titulo_pesquisado = self.request.POST['titulo_pesquisado']
        self.categoria_pesquisada = int(self.request.POST['categoria_pesquisada'])
        return render(request, self.template_name, {
            'titulo_pesquisado': self.titulo_pesquisado,
            'categoria_pesquisada': self.categoria_pesquisada,
            'categorias': Categoria.objects.all(),
            'noticias': self.get_queryset(),
        })

    def get_filtragem(self):
        filtragem = {}
        if self.titulo_pesquisado:
            filtragem['slug__contains'] = slugify(self.titulo_pesquisado)
        if self.categoria_pesquisada != 0:
            filtragem['categoria'] = int(self.categoria_pesquisada)
        if self.publicada:
            filtragem['publicada'] = self.publicada
        return filtragem

class HomeListView(NoticiasBaseListView):
    '''
    Listar as nóticias publicadas em home
    '''
    template_name = 'home.html'
    publicada = True

    def get_queryset(self):
        filtragem = self.get_filtragem()
        return Noticia.objects.filter(**filtragem).order_by('-publicada_em')

class NoticiasView(PermissionRequiredMixin, NoticiasBaseListView):
    '''
    Visualiza a área administrativa de notícias
    '''
    permission_required = "app_noticias.view_noticia"
    template_name = 'noticias_table.html'
   

    def get_queryset(self):
        user = self.request.user
        filtragem = self.get_filtragem()
        if not user.groups.filter(name='Editores').exists():
            filtragem['autor'] = user
        return Noticia.objects.filter(**filtragem).order_by('titulo')
        
    def get_success_url(self):
        return reverse('noticias')

class NoticiaBaseDetailView(DetailView):
    '''
    Classe Base dos detalhes da notícia
    '''
    model = Noticia
    template_name = 'noticia.html'

    def acrescentar_visualizacao(self, noticia_id: int = 0) -> None:
        '''
        Estrutura para uma classe filha implementar.
        '''
        pass

    def pode_ver_uma_noticia_nao_publicada(self) -> bool:
        '''
        Informa se pode ou não ver uma notícia.
        '''
        eh_editor: bool = self.request.user.has_perm('app_noticias.pode_publicar')
        eh_autor: bool = self.request.user.has_perm('app_noticias.add_noticia')
        eh_autor_da_noticia: bool = eh_autor and self.object.autor == self.request.user
        pode_ver_noticia_nao_publicada: bool = eh_editor or eh_autor_da_noticia
        return self.object.publicada or pode_ver_noticia_nao_publicada

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.pode_ver_uma_noticia_nao_publicada():
            raise PermissionDenied('Permissão para ver a notícia negada! Está notícia não foi publicada.')

        identificador = kwargs.get('pk', 0)
        self.acrescentar_visualizacao(identificador)

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class NoticiaDetailView(NoticiaBaseDetailView):
    '''
    Detalhe da notícia no Portal de Notícias
    '''

    def acrescentar_visualizacao(self, noticia_id: int = 0):
        '''
        Uma notícia visualizada no Portal de Notícias deve ser acrescentado
        o seu número de visualizações.
        '''
        if self.object.publicada and not noticia_id:
            self.object.num_visualizacoes += 1
            self.object.save()

class NoticiaAdmDetailView(PermissionRequiredMixin, NoticiaBaseDetailView):
    '''
    Detalhe da Notícia na Área Administrativa.
    '''
    permission_required = "app_noticias.view_noticia"

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
            raise PermissionDenied('Permissão para excluir a notícia negada! Você não possui permissão necessária.')
        if not eh_editor and self.object.autor != self.request.user:
            raise PermissionDenied('Permissão para excluir a notícia negada! Você não é o autor da notícia.')
        return super().form_valid(form)

    
    def get_success_url(self):
        return reverse('noticias')

@login_required(login_url="/accounts/login/")
@permission_required("app_noticias.pode_publicar")
def publicar_noticia(request, noticia_id: int, publicado: int) -> HttpResponse:
    '''
    Publicar Notícia
    '''
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    if publicado == 1:
        noticia.publicada = True
        noticia.publicada_em = datetime.now()
    else:
        noticia.publicada = False
        noticia.publicada_em = None
    noticia.save()
    return HttpResponseRedirect(reverse("noticias"))



class CategoriasView(PermissionRequiredMixin, ListView):
    '''
    Visualiza a área administrativa de categorias
    '''
    model = Categoria
    permission_required = "app_noticias.view_categoria"
    context_object_name = 'categorias'
    template_name = 'categorias_table.html'
      
    def get_success_url(self):
        return reverse('categorias')
    
class CadastrarCategoriaView(PermissionRequiredMixin, CreateView):
    '''
    Visualiza o cadastro de categoria na área administrativa de categorias
    '''
    model = Categoria
    form_class = CategoriaForm
    permission_required = "app_noticias.add_categoria"
    template_name = 'categoria_cadastro.html'

    def get_success_url(self):
        return reverse('categorias')
    
class EditarCategoriaView(PermissionRequiredMixin, UpdateView):
    '''
    Visualiza a edição de categoria na área administrativa de categorias
    '''
    model = Categoria
    # form_class = CategoriaForm
    fields = ['nome',  'imagem']
    permission_required = "app_noticias.change_categoria"
    template_name = 'categoria_cadastro.html'   

    def get_success_url(self):
        return reverse('categorias')
    

class ExcluirCategoriaView(PermissionRequiredMixin, DeleteView):
    '''
    Visualiza a decisão de deletar uma categoria na área administrativa de categorias
    '''
    model = Categoria
    permission_required = "app_noticias.delete_categoria"
    template_name = 'categoria_confirm_delete.html'
    context_object_name = 'categoria'

    def get_success_url(self):
        return reverse('categorias')