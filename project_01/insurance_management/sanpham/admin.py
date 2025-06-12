from django.contrib import admin
from .models import SanPham

@admin.register(SanPham)
class SanPhamAdmin(admin.ModelAdmin):
    list_display = ('ma_sp', 'ten_san_pham', 'loai_san_pham', 'trang_thai', 'phi_bao_hiem_toi_thieu', 'phi_bao_hiem_toi_da')
    list_filter = ('loai_san_pham', 'trang_thai')
    search_fields = ('ma_sp', 'ten_san_pham')
    readonly_fields = ('ma_sp',)
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('ma_sp', 'ten_san_pham', 'mo_ta', 'loai_san_pham', 'trang_thai')
        }),
        ('Thông tin tài chính', {
            'fields': (
                'phi_bao_hiem_toi_thieu', 'phi_bao_hiem_toi_da',
                'so_tien_bao_hiem_toi_thieu', 'so_tien_bao_hiem_toi_da'
            )
        }),
        ('Thời hạn và độ tuổi', {
            'fields': (
                'thoi_han_toi_thieu', 'thoi_han_toi_da',
                'tuoi_toi_thieu', 'tuoi_toi_da'
            )
        }),
        ('Phí quản lý', {
            'fields': ('ty_le_phi_quan_ly',)
        })
    )