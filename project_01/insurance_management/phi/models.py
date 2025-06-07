from django.db import models
from core.models import BaseModel
from sanpham.models import SanPham
from hopdong.models import HopDong
from decimal import Decimal
import uuid

class LoaiPhi(models.TextChoices):
    PHI_COI = 'phi_coi', 'Phí coi'
    PHI_QUAN_LY = 'phi_quan_ly', 'Phí quản lý'
    PHI_THANH_TOAN = 'phi_thanh_toan', 'Phí thanh toán'

class BangPhiCoi(BaseModel):
    """Bảng phí coi theo độ tuổi và mệnh giá"""
    ma_phi_coi = models.CharField(
        max_length=20,
        unique=True,
        primary_key=True,
        verbose_name='Mã phí coi'
    )
    san_pham = models.ForeignKey(
        SanPham,
        on_delete=models.CASCADE,
        related_name='bang_phi_coi',
        verbose_name='Sản phẩm'
    )
    
    # Độ tuổi áp dụng
    tuoi_tu = models.IntegerField(verbose_name='Tuổi từ')
    tuoi_den = models.IntegerField(verbose_name='Tuổi đến')
    
    # Mệnh giá áp dụng
    menh_gia_tu = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Mệnh giá từ'
    )
    menh_gia_den = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Mệnh giá đến'
    )
    
    # Tỷ lệ phí
    ty_le_phi = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        verbose_name='Tỷ lệ phí (%)'
    )
    phi_co_dinh = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0'),
        verbose_name='Phí cố định'
    )
    
    def save(self, *args, **kwargs):
        if not self.ma_phi_coi:
            self.ma_phi_coi = f"PC{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def tinh_phi(self, menh_gia):
        """Tính phí coi dựa trên mệnh giá"""
        phi_theo_ty_le = menh_gia * self.ty_le_phi / 100
        return phi_theo_ty_le + self.phi_co_dinh
    
    def __str__(self):
        return f"{self.ma_phi_coi} - {self.san_pham.ten_san_pham} ({self.tuoi_tu}-{self.tuoi_den} tuổi)"
    
    class Meta:
        verbose_name = 'Bảng phí coi'
        verbose_name_plural = 'Bảng phí coi'
        db_table = 'bang_phi_coi'

class PhiQuanLy(BaseModel):
    """Phí quản lý theo sản phẩm"""
    ma_phi_ql = models.CharField(
        max_length=20,
        unique=True,
        primary_key=True,
        verbose_name='Mã phí quản lý'
    )
    san_pham = models.OneToOneField(
        SanPham,
        on_delete=models.CASCADE,
        related_name='phi_quan_ly',
        verbose_name='Sản phẩm'
    )
    
    # Phí quản lý
    ty_le_phi_quan_ly = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        verbose_name='Tỷ lệ phí quản lý (%)'
    )
    phi_quan_ly_toi_thieu = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0'),
        verbose_name='Phí quản lý tối thiểu'
    )
    phi_quan_ly_toi_da = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Phí quản lý tối đa'
    )
    
    def save(self, *args, **kwargs):
        if not self.ma_phi_ql:
            self.ma_phi_ql = f"PQL{uuid.uuid4().hex[:7].upper()}"
        super().save(*args, **kwargs)
    
    def tinh_phi_quan_ly(self, phi_bao_hiem):
        """Tính phí quản lý dựa trên phí bảo hiểm"""
        phi_ql = phi_bao_hiem * self.ty_le_phi_quan_ly / 100
        
        # Áp dụng giới hạn tối thiểu
        phi_ql = max(phi_ql, self.phi_quan_ly_toi_thieu)
        
        # Áp dụng giới hạn tối đa nếu có
        if self.phi_quan_ly_toi_da:
            phi_ql = min(phi_ql, self.phi_quan_ly_toi_da)
        
        return phi_ql
    
    def __str__(self):
        return f"{self.ma_phi_ql} - {self.san_pham.ten_san_pham}"
    
    class Meta:
        verbose_name = 'Phí quản lý'
        verbose_name_plural = 'Phí quản lý'
        db_table = 'phi_quan_ly'

class PhiThanhToan(BaseModel):
    """Phí thanh toán theo hợp đồng"""
    ma_phi_tt = models.CharField(
        max_length=20,
        unique=True,
        primary_key=True,
        verbose_name='Mã phí thanh toán'
    )
    hop_dong = models.ForeignKey(
        HopDong,
        on_delete=models.CASCADE,
        related_name='phi_thanh_toan_list',
        verbose_name='Hợp đồng'
    )
    
    # Thông tin kỳ hạn
    thang_nam = models.DateField(verbose_name='Tháng năm áp dụng')
    
    # Phí thanh toán
    phi_bao_hiem = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Phí bảo hiểm'
    )
    phi_quan_ly = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0'),
        verbose_name='Phí quản lý'
    )
    phi_coi = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0'),
        verbose_name='Phí coi'
    )
    tong_phi = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Tổng phí'
    )
    
    # Thông tin thanh toán
    ngay_dao_han = models.DateField(verbose_name='Ngày đảo hạn')
    da_thanh_toan = models.BooleanField(default=False, verbose_name='Đã thanh toán')
    ngay_thanh_toan = models.DateField(null=True, blank=True, verbose_name='Ngày thanh toán')
    
    def save(self, *args, **kwargs):
        if not self.ma_phi_tt:
            self.ma_phi_tt = f"PTT{uuid.uuid4().hex[:7].upper()}"
        
        # Tự động tính tổng phí
        self.tong_phi = self.phi_bao_hiem + self.phi_quan_ly + self.phi_coi
        
        super().save(*args, **kwargs)
    
    @property
    def qua_han(self):
        """Kiểm tra có quá hạn thanh toán không"""
        from datetime import date
        return not self.da_thanh_toan and date.today() > self.ngay_dao_han
    
    def __str__(self):
        return f"{self.ma_phi_tt} - {self.hop_dong.ma_hd} - {self.thang_nam.strftime('%m/%Y')}"
    
    class Meta:
        verbose_name = 'Phí thanh toán'
        verbose_name_plural = 'Phí thanh toán'
        db_table = 'phi_thanh_toan'
        unique_together = ['hop_dong', 'thang_nam']
        ordering = ['-thang_nam']