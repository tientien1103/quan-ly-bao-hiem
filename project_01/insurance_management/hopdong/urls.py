from django.urls import path
from . import views

urlpatterns = [
    path('', views.HopDongListView.as_view(), name='hopdong-list'),
    path('<str:ma_hd>/', views.HopDongDetailView.as_view(), name='hopdong-detail'),
    path('<str:ma_hd>/tinh-phi/', views.HopDongTinhPhiView.as_view(), name='hopdong-tinh-phi'),
]