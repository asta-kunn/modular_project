from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Module, InstalledModule
from django.contrib import messages
from django.core.management import call_command
from django.utils import timezone

@login_required
def module_list_view(request):
    modules_qs = Module.objects.all()
    user_installed = InstalledModule.objects.filter(user=request.user)
    # Dictionary: key = module.slug, value = InstalledModule object
    user_installed_dict = {um.module.slug: um for um in user_installed}
    return render(request, 'engine/module_list.html', {
        'modules': modules_qs,
        'user_installed': user_installed_dict,
    })

@login_required
def install_module(request, slug):
    module = get_object_or_404(Module, slug=slug)
    installed, created = InstalledModule.objects.get_or_create(
         user=request.user, 
         module=module, 
         defaults={'installed_version': module.version}
    )
    if not created:
         messages.info(request, "Module sudah pernah diinstall.")
    else:
         messages.success(request, "Module berhasil diinstall.")
    return redirect('engine:module_list')

@login_required
def uninstall_module(request, slug):
    module = get_object_or_404(Module, slug=slug)
    try:
         installed_module = InstalledModule.objects.get(user=request.user, module=module)
         installed_module.delete()
         messages.success(request, "Module berhasil diuninstall.")
    except InstalledModule.DoesNotExist:
         messages.error(request, "Module belum diinstall.")
    return redirect('engine:module_list')

@login_required
def upgrade_module(request, slug):
    module = get_object_or_404(Module, slug=slug)
    try:
         installed_module = InstalledModule.objects.get(user=request.user, module=module)
    except InstalledModule.DoesNotExist:
         messages.error(request, "Module belum diinstall.")
         return redirect('engine:module_list')
    if installed_module.installed_version == module.version:
         messages.info(request, "Module sudah dalam versi terbaru.")
         return redirect('engine:module_list')
    try:
         # Jika ada kebutuhan khusus untuk module tertentu (contoh product_module)
         if slug == 'product-module':
             call_command('makemigrations', 'product_module', interactive=False, verbosity=0)
             call_command('migrate', 'product_module', interactive=False, verbosity=0)
         new_version = timezone.now().strftime('%d %B %Y, %I:%M %p')
         module.version = new_version
         module.save()
         installed_module.installed_version = new_version
         installed_module.save()
         messages.success(request, "Module upgraded successfully. Schema changes have been applied.")
    except Exception as e:
         messages.error(request, f"Module upgrade failed: {str(e)}")
    return redirect('engine:module_list')
