from django.urls import path
from . import views

app_name = 'product_module'

urlpatterns = [
    path('<slug:module_slug>/', views.landing, name='landing'),
    path('<slug:module_slug>/products/', views.product_list_view, name='product_list'),
    path('<slug:module_slug>/products/create/', views.product_create_view, name='product_create'),
    path('<slug:module_slug>/products/update/<int:pk>/', views.product_update_view, name='product_update'),
    path('<slug:module_slug>/products/delete/<int:pk>/', views.product_delete_view, name='product_delete'),
]
