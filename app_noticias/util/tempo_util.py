'''
Módulo utilitáriio para calculo de tempo.
'''
from datetime import datetime
from typing import Optional
from django.utils import timezone

def calcular_tempo_decorrido(data_hora: Optional[datetime]) -> str:
    '''
    Calculo do tempo decorrido:
    Tempo atual menos a data e hora informada.
    '''
    if not data_hora:
        return ''
    tempo_decorrido = timezone.now() - data_hora
    tempo_decorrido_formatado = '%d:%d' % (
        tempo_decorrido.seconds // 3600, # Minutos
        tempo_decorrido.seconds // 60 % 60, # Horas
    )
    tempos = tempo_decorrido_formatado.split(':')
    horas = tempos[0]
    minutos = tempos[1]

    horas_texto = ''
    minutos_texto = ''

    if horas == '1':
        horas_texto = f"{horas} hora"
    elif horas != '0':
        horas_texto = f"{horas} horas"

    if minutos == '1':
        minutos_texto = f"{minutos} minuto"
    elif minutos != '0':
        minutos_texto = f"{minutos} minutos"

    horas_e_minutos_texto = ''

    if horas_texto and minutos_texto:
        horas_e_minutos_texto =  f"{horas_texto} e {minutos_texto}"
    elif horas_texto:
        horas_e_minutos_texto =  f"{horas_texto}"
    elif minutos_texto:
        horas_e_minutos_texto =  f"{minutos_texto}"
    else:
        horas_e_minutos_texto =  'agora'

    if tempo_decorrido.days == 1:
        return f"{tempo_decorrido.days} dia"
    if tempo_decorrido.days > 1:
        return f"{tempo_decorrido.days} dias"

    return horas_e_minutos_texto
