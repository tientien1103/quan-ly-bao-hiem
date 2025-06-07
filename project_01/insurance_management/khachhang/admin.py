from django.contrib import admin
from .models import KhachHang

@admin.register(KhachHang)
class KhachHangAdmin(admin.ModelAdmin):
    list_display = ('ma_kh', 'ho_ten', 'so_dien_thoai', 'email', 'trang_thai', 'ngay_dang_ky')
    list_filter = ('trang_thai', 'gioi_tinh', 'ngay_dang_ky')
    search_fields = ('ma_kh', 'ho_ten', 'so_cmnd', 'so_dien_thoai', 'email')
    readonly_fields = ('ma_kh', 'tuoi', 'ngay_dang_ky')
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('ma_kh', 'user', 'ho_ten', 'ngay_sinh', 'tuoi', 'gioi_tinh')
        }),
        ('Giấy tờ tùy thân', {
            'fields': ('so_cmnd', 'ngay_cap_cmnd', 'noi_cap_cmnd')
        }),
        ('Thông tin liên hệ', {
            'fields': ('so_dien_thoai', 'email', 'dia_chi')
        }),
        ('Thông tin nghề nghiệp', {
            'fields': ('nghe_nghiep', 'noi_lam_viec', 'thu_nhap_hang_thang')
        }),
        ('Thông tin bảo hiểm', {
            'fields': ('trang_thai', 'ngay_dang_ky')
        }),
        ('Người thụ hưởng', {
            'fields': ('ten_nguoi_thu_huong', 'quan_he_nguoi_thu_huong')
        })
    )