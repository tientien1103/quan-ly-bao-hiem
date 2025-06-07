from django.contrib import admin
from .models import ThanhToan, CongNo

@admin.register(ThanhToan)
class ThanhToanAdmin(admin.ModelAdmin):
    list_display = ('ma_thanh_toan', 'hop_dong', 'so_tien', 'phuong_thuc_thanh_toan', 'trang_thai', 'ngay_thanh_toan')
    list_filter = ('trang_thai', 'phuong_thuc_thanh_toan', 'ngay_thanh_toan')
    search_fields = ('ma_thanh_toan', 'hop_dong__ma_hd', 'ma_giao_dich_ngan_hang')
    readonly_fields = ('ma_thanh_toan',)

@admin.register(CongNo)
class CongNoAdmin(admin.ModelAdmin):
    list_display = ('ma_cong_no', 'hop_dong', 'so_tien_no', 'ngay_dao_han', 'da_thanh_toan', 'so_ngay_tre_han', 'tong_cong_no')
    list_filter = ('da_thanh_toan', 'ngay_phat_sinh')
    search_fields = ('ma_cong_no', 'hop_dong__ma_hd')
    readonly_fields = ('ma_cong_no', 'so_ngay_tre_han', 'tong_cong_no')