'''
MODELS app_noticias
'''
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User, AbstractUser


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
    autor = models.ForeignKey(User, on_delete=models.RESTRICT, editable=False)
    categoria = models.ManyToManyField(Categoria)
    publicada_em = models.DateTimeField('Publicada em', help_text='dd/mm/yyyy hh:MM', null=True, editable=False)
    publicada = models.BooleanField('Publicada', default=False)

    def save(self, *args, **kwargs):
        if self.publicada and not self.publicada_em:
            self.publicada_em = datetime.now()
        elif not self.publicada and self.publicada_em:
            self.publicada_em = None
        return super().save(*args, **kwargs)

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

