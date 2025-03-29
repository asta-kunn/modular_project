from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from engine.models import Module, InstalledModule
from .models import Product

def get_user_role(request):
    """
    Mengembalikan role user ('manager', 'user', atau 'public').
    """
    try:
        return request.user.userprofile.role
    except Exception:
        return 'public'

@login_required
def landing(request, module_slug):
    try:
        module = Module.objects.get(slug=module_slug)
        InstalledModule.objects.get(user=request.user, module=module)
    except (Module.DoesNotExist, InstalledModule.DoesNotExist):
        raise Http404("Module tidak diinstall")
    return render(request, 'product_module/landing.html', {'module': module})


@login_required
def product_list_view(request, module_slug):
    """
    Menampilkan daftar produk untuk modul tertentu.
    Hanya produk yang terkait dengan modul yang ditampilkan.
    """
    try:
        module = Module.objects.get(slug=module_slug)
        InstalledModule.objects.get(user=request.user, module=module)
    except (Module.DoesNotExist, InstalledModule.DoesNotExist):
        raise Http404("Module tidak diinstall")

    products = Product.objects.filter(module=module)
    role = get_user_role(request)
    return render(request, 'product_module/product_list.html', {
        'products': products,
        'role': role,
        'module': module
    })

@login_required
def product_create_view(request, module_slug):
    """
    Menangani pembuatan produk untuk modul tertentu.
    Jika user (baik manager maupun user) yang melakukan operasi, maka
    global version dan installed version (untuk user yang mengedit) diupdate otomatis.
    """
    role = get_user_role(request)
    if role not in ['manager', 'user']:
        messages.error(request, "Anda tidak memiliki izin untuk membuat produk.")
        return redirect('product_module:product_list', module_slug=module_slug)
    
    module = get_object_or_404(Module, slug=module_slug)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        barcode = request.POST.get('barcode')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        if name and barcode and price and stock:
            try:
                Product.objects.create(
                    module=module,
                    name=name,
                    barcode=barcode,
                    price=price,
                    stock=stock
                )
                new_version = timezone.now().strftime('%d %B %Y, %I:%M %p')
                module.version = new_version
                module.save()
                # Update installed version untuk user yang melakukan operasi (editor)
                installed_module = InstalledModule.objects.get(user=request.user, module=module)
                installed_module.installed_version = new_version
                installed_module.save()
                messages.success(request, "Produk berhasil dibuat!")
            except Exception as e:
                messages.error(request, f"Error saat membuat produk: {str(e)}")
            return redirect('product_module:product_list', module_slug=module_slug)
    
    return render(request, 'product_module/product_form.html', {
        'action': 'create',
        'module_slug': module_slug
    })

@login_required
def product_update_view(request, module_slug, pk):
    """
    Menangani update produk untuk modul tertentu.
    Setelah update, global version diupdate dan installed version untuk user yang melakukan update juga diupdate otomatis.
    """
    role = get_user_role(request)
    if role not in ['manager', 'user']:
        messages.error(request, "Anda tidak memiliki izin untuk mengubah produk.")
        return redirect('product_module:product_list', module_slug=module_slug)
    
    module = get_object_or_404(Module, slug=module_slug)
    product = get_object_or_404(Product, pk=pk, module=module)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.barcode = request.POST.get('barcode')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        try:
            product.save()
            new_version = timezone.now().strftime('%d %B %Y, %I:%M %p')
            module.version = new_version
            module.save()
            installed_module = InstalledModule.objects.get(user=request.user, module=module)
            installed_module.installed_version = new_version
            installed_module.save()
            messages.success(request, "Produk berhasil diupdate!")
        except Exception as e:
            messages.error(request, f"Error saat update produk: {str(e)}")
        return redirect('product_module:product_list', module_slug=module_slug)
    
    return render(request, 'product_module/product_form.html', {
        'action': 'update',
        'product': product,
        'module_slug': module_slug
    })

@login_required
def product_delete_view(request, module_slug, pk):
    """
    Menangani penghapusan produk untuk modul tertentu.
    Hanya user dengan role 'manager' yang dapat menghapus produk.
    Setelah delete, global version diupdate dan installed version untuk user yang melakukan delete juga diupdate otomatis.
    """
    role = get_user_role(request)
    if role != 'manager':
        messages.error(request, "Anda tidak memiliki izin untuk menghapus produk.")
        return redirect('product_module:product_list', module_slug=module_slug)
    
    module = get_object_or_404(Module, slug=module_slug)
    product = get_object_or_404(Product, pk=pk, module=module)
    
    if request.method == 'POST':
        try:
            product.delete()
            new_version = timezone.now().strftime('%d %B %Y, %I:%M %p')
            module.version = new_version
            module.save()
            installed_module = InstalledModule.objects.get(user=request.user, module=module)
            installed_module.installed_version = new_version
            installed_module.save()
            messages.success(request, "Produk berhasil dihapus!")
        except Exception as e:
            messages.error(request, f"Error saat menghapus produk: {str(e)}")
        return redirect('product_module:product_list', module_slug=module_slug)
    
    return render(request, 'product_module/product_confirm_delete.html', {
        'product': product,
        'module': module
    })
