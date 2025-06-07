from django.db import models
from core.models import BaseModel
from decimal import Decimal
import uuid

class LoaiSanPham(models.TextChoices):
    BAO_HIEM_NHAN_THO = 'nhan_tho', 'Bảo hiểm nhân thọ'
    BAO_HIEM_SUC_KHOE = 'suc_khoe', 'Bảo hiểm sức khỏe'
    BAO_HIEM_XE_CO = 'xe_co', 'Bảo hiểm xe cơ giới'
    BAO_HIEM_NHA_O = 'nha_o', 'Bảo hiểm nhà ở'
    BAO_HIEM_DU_LICH = 'du_lich', 'Bảo hiểm du lịch'
    BAO_HIEM_DOANH_NGHIEP = 'doanh_nghiep', 'Bảo hiểm doanh nghiệp'

class TrangThaiSanPham(models.TextChoices):
    HOAT_DONG = 'hoat_dong', 'Hoạt động'
    TAM_DUNG = 'tam_dung', 'Tạm dừng'
    NGUNG_BAN = 'ngung_ban', 'Ngừng bán'

class SanPham(BaseModel):
    """Model sản phẩm bảo hiểm"""
    ma_sp = models.CharField(
        max_length=20,
        unique=True,
        primary_key=True,
        verbose_name='Mã sản phẩm'
    )
    
    # Thông tin cơ bản
    ten_san_pham = models.CharField(max_length=200, verbose_name='Tên sản phẩm')
    mo_ta = models.TextField(verbose_name='Mô tả')
    loai_san_pham = models.CharField(
        max_length=20,
        choices=LoaiSanPham.choices,
        verbose_name='Loại sản phẩm'
    )
    
    # Thông tin tài chính
    phi_bao_hiem_toi_thieu = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Phí bảo hiểm tối thiểu'
    )
    phi_bao_hiem_toi_da = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Phí bảo hiểm tối đa'
    )
    so_tien_bao_hiem_toi_thieu = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Số tiền bảo hiểm tối thiểu'
    )
    so_tien_bao_hiem_toi_da = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Số tiền bảo hiểm tối đa'
    )
    
    # Thông tin thời hạn
    thoi_han_toi_thieu = models.IntegerField(
        verbose_name='Thời hạn tối thiểu (tháng)'
    )
    thoi_han_toi_da = models.IntegerField(
        verbose_name='Thời hạn tối đa (tháng)'
    )
    
    # Độ tuổi áp dụng
    tuoi_toi_thieu = models.IntegerField(verbose_name='Tuổi tối thiểu')
    tuoi_toi_da = models.IntegerField(verbose_name='Tuổi tối đa')
    
    # Thông tin khác
    ty_le_phi_quan_ly = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=Decimal('0.0500'),
        verbose_name='Tỷ lệ phí quản lý (%)'
    )
    trang_thai = models.CharField(
        max_length=20,
        choices=TrangThaiSanPham.choices,
        default=TrangThaiSanPham.HOAT_DONG,
        verbose_name='Trạng thái'
    )
    
    def save(self, *args, **kwargs):
        if not self.ma_sp:
            # Tự động tạo mã sản phẩm
            prefix = {
                'nhan_tho': 'NT',
                'suc_khoe': 'SK',
                'xe_co': 'XC',
                'nha_o': 'NO',
                'du_lich': 'DL',
                'doanh_nghiep': 'DN'
            }.get(self.loai_san_pham, 'SP')
            self.ma_sp = f"{prefix}{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)
    
    def tinh_phi_co_ban(self, tuoi, so_tien_bao_hiem):
        """Tính phí cơ bản dựa trên tuổi và số tiền bảo hiểm"""
        if tuoi < self.tuoi_toi_thieu or tuoi > self.tuoi_toi_da:
            raise ValueError("Tuổi không phù hợp với sản phẩm")
        
        # Công thức tính phí cơ bản (có thể tùy chỉnh)
        he_so_tuoi = 1 + (tuoi - 25) * Decimal('0.02')
        phi_co_ban = so_tien_bao_hiem * Decimal('0.01') * he_so_tuoi
        
        return max(self.phi_bao_hiem_toi_thieu, 
                  min(phi_co_ban, self.phi_bao_hiem_toi_da))
    
    def __str__(self):
        return f"{self.ma_sp} - {self.ten_san_pham}"
    
    class Meta:
        verbose_name = 'Sản phẩm bảo hiểm'
        verbose_name_plural = 'Sản phẩm bảo hiểm'
        db_table = 'san_pham'
        ordering = ['ten_san_pham']