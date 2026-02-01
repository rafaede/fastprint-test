from django.urls import path
from . import views

urlpatterns = [
    path('', views.produk_list, name='produk_list'),
    path('tambah/', views.produk_tambah, name='produk_tambah'),
    path('edit/<int:pk>/', views.produk_edit, name='produk_edit'),
    path('hapus/<int:pk>/', views.produk_hapus, name='produk_hapus'),
]