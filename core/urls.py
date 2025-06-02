from django.urls import path
from core.views.customer import (
    create_khachhang,
    get_khachhang,
    list_khachhang,
    update_khachhang,
    delete_khachhang
)
from core.views.product import (
    list_sanpham,
    get_sanpham,
    get_phi_coi,
    create_phi_coi,
    get_phi_quanly
)
from core.views.contract import (
    create_hopdong,
    get_hopdong,
    list_hopdong,
    update_hopdong,
    tinh_phi
)
from core.views.payment import (
    get_danh_sach_phi,
    tao_phi_thang,
    list_lich_su_thanhtoan,
    create_thanhtoan,
    get_thanh_toan
)
from core.views.account import register, login, get_current_user

urlpatterns = [
    # Customer
    path('khachhang/', create_khachhang, name='create-khachhang'),
    path('khachhang/<str:ma_kh>/', get_khachhang, name='get-khachhang'),
    path('khachhang/', list_khachhang, name='list-khachhang'),
    path('khachhang/<str:ma_kh>/', update_khachhang, name='update-khachhang'),
    path('khachhang/<str:ma_kh>/', delete_khachhang, name='delete-khachhang'),
    
    # Product
    path('sanpham/', list_sanpham, name='list-sanpham'),
    path('sanpham/<str:ma_sp>/', get_sanpham, name='get-sanpham'),
    path('phi-coi/<str:ma_sp>/<int:tuoi>/<int:menh_gia>/', get_phi_coi, name='get-phi-coi'),
    path('phi-coi/', create_phi_coi, name='create-phi-coi'),
    path('phi-quan-ly/<str:ma_sp>/', get_phi_quanly, name='get-phi-quanly'),
    
    # Contract
    path('hopdong/', create_hopdong, name='create-hopdong'),
    path('hopdong/<str:ma_hd>/', get_hopdong, name='get-hopdong'),
    path('hopdong/', list_hopdong, name='list-hopdong'),
    path('hopdong/<str:ma_hd>/', update_hopdong, name='update-hopdong'),
    path('hopdong/<str:ma_hd>/tinh-phi/<str:thang_nam>/', tinh_phi, name='tinh-phi'),
    
    # Payment
    path('phi-thanhtoan/<str:ma_hd>/', get_danh_sach_phi, name='get-danh-sach-phi'),
    path('phi-thanhtoan/', tao_phi_thang, name='tao-phi-thang'),
    path('thanh-toan/<str:ma_hd>/', list_lich_su_thanhtoan, name='list-lich-su-thanhtoan'),
    path('thanh-toan/', create_thanhtoan, name='create-thanhtoan'),
    path('thanh-toan/<str:ma_hd>/', get_thanh_toan, name='get-thanh-toan'),
    
    # Auth
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/me/', get_current_user, name='current-user'),
]