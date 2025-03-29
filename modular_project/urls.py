from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    return redirect('engine:module_list')

urlpatterns = [
    path('', home_redirect, name='/accounts/login/'),
    path('admin/', admin.site.urls),
    path('module/', include('engine.urls', namespace='engine')),
    path('product/', include('product_module.urls', namespace='product_module')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
]
