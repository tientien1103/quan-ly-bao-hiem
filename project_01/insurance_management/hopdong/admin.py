from django.contrib import admin
from .models import HopDong

@admin.register(HopDong)
class HopDongAdmin(admin.ModelAdmin):
    list_display = ('ma_hd', 'khach_hang', 'san_pham', 'trang_thai', 'ngay_ky', 'so_tien_bao_hiem')
    list_filter = ('trang_thai', 'ky_han_dong_phi', 'ngay_ky')
    search_fields = ('ma_hd', 'khach_hang__ho_ten', 'san_pham__ten_san_pham')
    readonly_fields = ('ma_hd', 'so_thang_hieu_luc', 'is_hieu_luc')
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('ma_hd', 'khach_hang', 'san_pham', 'nhan_vien_ban')
        }),
        ('Thời gian', {
            'fields': ('ngay_ky', 'ngay_hieu_luc', 'ngay_ket_thuc', 'so_thang_hieu_luc')
        }),
        ('Thông tin tài chính', {
            'fields': ('so_tien_bao_hiem', 'phi_bao_hiem', 'ky_han_dong_phi')
        }),
        ('Trạng thái', {
            'fields': ('trang_thai', 'is_hieu_luc')
        }),
        ('Người thụ hưởng', {
            'fields': ('ten_nguoi_thu_huong', 'quan_he_nguoi_thu_huong')
        }),
        ('Ghi chú', {
            'fields': ('ghi_chu',)
        })
    )