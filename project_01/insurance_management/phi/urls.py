from django.urls import path
from . import views

urlpatterns = [
    path('coi/', views.PhiCoiView.as_view(), name='phi-coi'),
    path('quan-ly/<str:ma_sp>/', views.PhiQuanLyView.as_view(), name='phi-quan-ly'),
    path('thanhtoan/tao-moi/', views.TaoPhiThanhToanView.as_view(), name='tao-phi-thanhtoan'),
    path('thanhtoan/<str:ma_hd>/', views.PhiThanhToanView.as_view(), name='phi-thanhtoan'),
]
