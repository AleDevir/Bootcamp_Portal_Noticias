# Intalação das bibliotecas (requirements.txt)
´´´
...
gunicorn
whitenoise[brotli]
´´´


# Procedimento Deploy
´´´
# 1. Renomear a pasta static para staticfiles

# 2. Mover a pasta /media para /staticfiles

# 3. No arquivo settings.py acrescentar:
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    ...
    ...
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
    ...
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 4. Executar
python manage.py collectstatic --no-input

# 5. Subir a aplicação para testar:
python manage.py runserver

´´´