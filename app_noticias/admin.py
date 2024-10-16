'''
ADMIN: Registrar modelos da aplicação na área administrativa.
'''

from django.contrib import admin


from .models import (

    Categoria,
    Noticia
)

class NoticiaAdmin(admin.ModelAdmin):
    '''
    NoticiaAdmin
    '''
    list_display = [
        'titulo',
        'criada_em',
        'atualizada_em',
        'publicada',
        'publicada_em',
        'imagem',
        'autor',
        'categoria'
    ]
    list_filter = ['publicada']
    search_fields = ['titulo']


admin.site.register(Noticia, NoticiaAdmin)

admin.site.register([
    Categoria,
])
