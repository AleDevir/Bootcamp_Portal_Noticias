'''
MODELS app_noticias
'''

from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    '''
    Categoria
    '''
    nome = models.CharField('Categoria', max_length=30, unique=True)
    criado_em = models.DateField(auto_now_add=True)
    def __str__(self):
        '''
        str
        '''
        return str(self.nome)

class Noticia(models.Model):
    '''
    Noticia
    '''
    titulo = models.CharField('Título', max_length=100, unique=True)
    conteudo= models.TextField('Conteúdo', max_length=3000)
    criada_em = models.DateTimeField('Criada em', help_text='dd/mm/yyyy hh:MM', auto_now_add=True)
    atualizada_em = models.DateTimeField('Atualizada', help_text='dd/mm/yyyy hh:MM', auto_now_add=True)
    imagem = models.ImageField(upload_to='', blank=True)
    autor = models.ForeignKey(User, on_delete=models.RESTRICT)
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT)
    publicada_em = models.DateTimeField('Publicada em', help_text='dd/mm/yyyy hh:MM', null=True)
    publicada = models.BooleanField('Publicada', default=False )

    class Meta:
        '''
        Metamodelo
        '''
        db_table = 'noticias'
       

    def __str__(self):
        '''
        str
        '''
        if self.publicada:
            return  f"Título: {str(self.titulo)} - PUBLICADA"
        return f"Título: {str(self.titulo)}"
        
