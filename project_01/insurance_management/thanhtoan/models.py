from django.db import models
from django.contrib.auth import get_user_model
from core.models import BaseModel
from hopdong.models import HopDong
from phi.models import PhiThanhToan
from decimal import Decimal
import uuid

User = get_user_model()

class PhuongThucThanhToan(models.TextChoices):
    TIEN_MAT = 'tien_mat', 'Tiền mặt'
    CHUYEN_KHOAN = 'chuyen_khoan', 'Chuyển khoản'
    THE_TIN_DUNG = 'the_tin_dung', 'Thẻ tín dụng'
    VI_DIEN_TU = 'vi_dien_tu', 'Ví điện tử'
    INTERNET_BANKING = 'internet_banking', 'Internet Banking'

class TrangThaiThanhToan(models.TextChoices):
    CHO_XU_LY = 'cho_xu_ly', 'Chờ xử lý'
    THANH_CONG = 'thanh_cong', 'Thành công'
    THAT_BAI = 'that_bai', 'Thất bại'
    HUY_BO = 'huy_bo', 'Hủy bỏ'

class ThanhToan(BaseModel):
    """Model giao dịch thanh toán"""
    ma_thanh_toan = models.CharField(
        max_length=20,
        unique=True,
        primary_key=True,
        verbose_name='Mã thanh toán'
    )
    
    # Thông tin liên kết
    hop_dong = models.ForeignKey(
        HopDong,
        on_delete=models.CASCADE,
        related_name='thanh_toan_list',
        verbose_name='Hợp đồng'
    )
    phi_thanh_toan = models.ForeignKey(
        PhiThanhToan,
        on_delete=models.CASCADE,
        related_name='thanh_toan_list',
        verbose_name='Phí thanh toán'
    )
    
    # Thông tin thanh toán
    so_tien = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Số tiền thanh toán'
    )
    phuong_thuc_thanh_toan = models.CharField(
        max_length=20,
        choices=PhuongThucThanhToan.choices,
        verbose_name='Phương thức thanh toán'
    )
    ngay_thanh_toan = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Ngày thanh toán'
    )
    
    # Trạng thái
    trang_thai = models.CharField(
        max_length=20,
        choices=TrangThaiThanhToan.choices,
        default=TrangThaiThanhToan.CHO_XU_LY,
        verbose_name='Trạng thái'
    )
    
    # Thông tin giao dịch
    ma_giao_dich_ngan_hang = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Mã giao dịch ngân hàng'
    )
    ten_ngan_hang = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Tên ngân hàng'
    )
    
    # Nhân viên xử lý
    nhan_vien_xu_ly = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='thanh_toan_xu_ly',
        verbose_name='Nhân viên xử lý'
    )
    
    # Ghi chú
    ghi_chu = models.TextField(blank=True, verbose_name='Ghi chú')
    ly_do_that_bai = models.TextField(blank=True, verbose_name='Lý do thất bại')
    
    def save(self, *args, **kwargs):
        if not self.ma_thanh_toan:
            # Tự động tạo mã thanh toán
            self.ma_thanh_toan = f"TT{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
        
        # Cập nhật trạng thái phí thanh toán
        if self.trang_thai == TrangThaiThanhToan.THANH_CONG:
            self.phi_thanh_toan.da_thanh_toan = True
            self.phi_thanh_toan.ngay_thanh_toan = self.ngay_thanh_toan.date()
            self.phi_thanh_toan.save()
    
    def __str__(self):
        return f"{self.ma_thanh_toan} - {self.hop_dong.ma_hd} - {self.so_tien:,.0f} VND"
    
    class Meta:
        verbose_name = 'Thanh toán'
        verbose_name_plural = 'Thanh toán'
        db_table = 'thanh_toan'
        ordering = ['-ngay_thanh_toan']

class CongNo(BaseModel):
    """Model công nợ của khách hàng"""
    ma_cong_no = models.CharField(
        max_length=20,
        unique=True,
        primary_key=True,
        verbose_name='Mã công nợ'
    )
    
    # Thông tin liên kết
    hop_dong = models.ForeignKey(
        HopDong,
        on_delete=models.CASCADE,
        related_name='cong_no_list',
        verbose_name='Hợp đồng'
    )
    
    # Thông tin công nợ
    so_tien_no = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Số tiền nợ'
    )
    ngay_phat_sinh = models.DateField(verbose_name='Ngày phát sinh')
    ngay_dao_han = models.DateField(verbose_name='Ngày đáo hạn')
    
    # Trạng thái
    da_thanh_toan = models.BooleanField(default=False, verbose_name='Đã thanh toán')
    ngay_thanh_toan = models.DateField(null=True, blank=True, verbose_name='Ngày thanh toán')
    
    # Phí phạt
    phi_tre_han = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0'),
        verbose_name='Phí trễ hạn'
    )
    ty_le_phi_tre_han = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=Decimal('0.0500'),
        verbose_name='Tỷ lệ phí trễ hạn (%/ngày)'
    )
    
    # Ghi chú
    ghi_chu = models.TextField(blank=True, verbose_name='Ghi chú')
    
    def save(self, *args, **kwargs):
        if not self.ma_cong_no:
            # Tự động tạo mã công nợ
            self.ma_cong_no = f"CN{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def so_ngay_tre_han(self):
        """Tính số ngày trễ hạn"""
        from datetime import date
        if self.da_thanh_toan:
            if self.ngay_thanh_toan and self.ngay_thanh_toan > self.ngay_dao_han:
                return (self.ngay_thanh_toan - self.ngay_dao_han).days
            return 0
        else:
            today = date.today()
            if today > self.ngay_dao_han:
                return (today - self.ngay_dao_han).days
            return 0
    
    @property
    def tong_cong_no(self):
        """Tính tổng công nợ bao gồm phí trễ hạn"""
        phi_tre_han_tinh_toan = self.so_tien_no * self.ty_le_phi_tre_han / 100 * self.so_ngay_tre_han
        return self.so_tien_no + phi_tre_han_tinh_toan + self.phi_tre_han
    
    def __str__(self):
        return f"{self.ma_cong_no} - {self.hop_dong.ma_hd} - {self.so_tien_no:,.0f} VND"
    
    class Meta:
        verbose_name = 'Công nợ'
        verbose_name_plural = 'Công nợ'
        db_table = 'cong_no'
        ordering = ['-ngay_phat_sinh']