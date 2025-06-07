from django.urls import path
from . import views

urlpatterns = [
    path('', views.ThanhToanListView.as_view(), name='thanh-toan-list'),
    path('<str:ma_hd>/', views.ThanhToanDetailView.as_view(), name='thanh-toan-detail'),
    path('con-no/<str:ma_hd>/', views.ConNoView.as_view(), name='con-no'),
]