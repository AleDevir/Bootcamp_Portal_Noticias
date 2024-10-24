def user_permissions(request):
    return {
        'is_editor': request.user.groups.filter(name='Editores').exists(),
        'is_author': request.user.groups.filter(name='Autores').exists(),
    }