from django.urls import path
from . import views

urlpatterns = [
    path('', views.KhachHangListView.as_view(), name='khachhang-list'),
    path('<str:ma_kh>/', views.KhachHangDetailView.as_view(), name='khachhang-detail'),
]