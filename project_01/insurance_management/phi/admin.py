from django.contrib import admin
from .models import BangPhiCoi, PhiQuanLy, PhiThanhToan

@admin.register(BangPhiCoi)
class BangPhiCoiAdmin(admin.ModelAdmin):
    list_display = ('ma_phi_coi', 'san_pham', 'tuoi_tu', 'tuoi_den', 'ty_le_phi', 'phi_co_dinh')
    list_filter = ('san_pham__loai_san_pham',)
    search_fields = ('ma_phi_coi', 'san_pham__ten_san_pham')

@admin.register(PhiQuanLy)
class PhiQuanLyAdmin(admin.ModelAdmin):
    list_display = ('ma_phi_ql', 'san_pham', 'ty_le_phi_quan_ly', 'phi_quan_ly_toi_thieu')
    search_fields = ('ma_phi_ql', 'san_pham__ten_san_pham')

@admin.register(PhiThanhToan)
class PhiThanhToanAdmin(admin.ModelAdmin):
    list_display = ('ma_phi_tt', 'hop_dong', 'thang_nam', 'tong_phi', 'da_thanh_toan', 'qua_han')
    list_filter = ('da_thanh_toan', 'thang_nam')
    search_fields = ('ma_phi_tt', 'hop_dong__ma_hd')
    readonly_fields = ('tong_phi', 'qua_han')