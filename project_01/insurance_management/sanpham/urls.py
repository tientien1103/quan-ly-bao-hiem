from django.urls import path
from . import views

urlpatterns = [
    path('', views.SanPhamListView.as_view(), name='sanpham-list'),
    path('<str:ma_sp>/', views.SanPhamDetailView.as_view(), name='sanpham-detail'),
]