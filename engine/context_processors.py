from .models import InstalledModule

def installed_modules(request):
    if request.user.is_authenticated:
         user_modules = InstalledModule.objects.filter(user=request.user)
         return {'user_installed_modules': {um.module.slug: um for um in user_modules}}
    return {}
