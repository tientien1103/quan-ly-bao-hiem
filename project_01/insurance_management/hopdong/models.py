from django.db import models
from django.contrib.auth import get_user_model
from core.models import BaseModel
from khachhang.models import KhachHang
from sanpham.models import SanPham
from decimal import Decimal
import uuid
from datetime import date, timedelta

User = get_user_model()

class TrangThaiHopDong(models.TextChoices):
    CHO_DUYET = 'cho_duyet', 'Chờ duyệt'
    HOAT_DONG = 'hoat_dong', 'Hoạt động'
    TAM_DUNG = 'tam_dung', 'Tạm dừng'
    HET_HAN = 'het_han', 'Hết hạn'
    HUY_BO = 'huy_bo', 'Hủy bỏ'

class KyHanDongPhi(models.TextChoices):
    HANG_THANG = 'hang_thang', 'Hàng tháng'
    HANG_QUY = 'hang_quy', 'Hàng quý'
    HANG_NAM = 'hang_nam', 'Hàng năm'
    MOT_LAN = 'mot_lan', 'Một lần'

class HopDong(BaseModel):
    """Model hợp đồng bảo hiểm"""
    ma_hd = models.CharField(
        max_length=20,
        unique=True,
        primary_key=True,
        verbose_name='Mã hợp đồng'
    )
    
    # Thông tin liên kết
    khach_hang = models.ForeignKey(
        KhachHang,
        on_delete=models.CASCADE,
        related_name='hop_dong_list',
        verbose_name='Khách hàng'
    )
    san_pham = models.ForeignKey(
        SanPham,
        on_delete=models.CASCADE,
        related_name='hop_dong_list',
        verbose_name='Sản phẩm'
    )
    nhan_vien_ban = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hop_dong_ban',
        verbose_name='Nhân viên bán'
    )
    
    # Thông tin hợp đồng
    ngay_ky = models.DateField(default=date.today, verbose_name='Ngày ký')
    ngay_hieu_luc = models.DateField(verbose_name='Ngày hiệu lực')
    ngay_ket_thuc = models.DateField(verbose_name='Ngày kết thúc')
    
    # Thông tin tài chính
    so_tien_bao_hiem = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Số tiền bảo hiểm'
    )
    phi_bao_hiem = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Phí bảo hiểm'
    )
    ky_han_dong_phi = models.CharField(
        max_length=20,
        choices=KyHanDongPhi.choices,
        default=KyHanDongPhi.HANG_THANG,
        verbose_name='Kỳ hạn đóng phí'
    )
    
    # Trạng thái
    trang_thai = models.CharField(
        max_length=20,
        choices=TrangThaiHopDong.choices,
        default=TrangThaiHopDong.CHO_DUYET,
        verbose_name='Trạng thái'
    )
    
    # Thông tin người thụ hưởng
    ten_nguoi_thu_huong = models.CharField(
        max_length=100,
        verbose_name='Tên người thụ hưởng'
    )
    quan_he_nguoi_thu_huong = models.CharField(
        max_length=50,
        verbose_name='Quan hệ với người thụ hưởng'
    )
    
    # Ghi chú
    ghi_chu = models.TextField(blank=True, verbose_name='Ghi chú')
    
    def save(self, *args, **kwargs):
        if not self.ma_hd:
            # Tự động tạo mã hợp đồng
            self.ma_hd = f"HD{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def so_thang_hieu_luc(self):
        """Tính số tháng hiệu lực của hợp đồng"""
        delta = self.ngay_ket_thuc - self.ngay_hieu_luc
        return delta.days // 30
    
    @property
    def is_hieu_luc(self):
        """Kiểm tra hợp đồng có hiệu lực không"""
        today = date.today()
        return (
            self.trang_thai == TrangThaiHopDong.HOAT_DONG and
            self.ngay_hieu_luc <= today <= self.ngay_ket_thuc
        )
    
    def tinh_phi_hang_thang(self, thang_nam=None):
        """Tính phí hàng tháng cần đóng"""
        if self.ky_han_dong_phi == KyHanDongPhi.HANG_THANG:
            return self.phi_bao_hiem
        elif self.ky_han_dong_phi == KyHanDongPhi.HANG_QUY:
            return self.phi_bao_hiem / 3
        elif self.ky_han_dong_phi == KyHanDongPhi.HANG_NAM:
            return self.phi_bao_hiem / 12
        else:  # MOT_LAN
            return Decimal('0')
    
    def __str__(self):
        return f"{self.ma_hd} - {self.khach_hang.ho_ten} - {self.san_pham.ten_san_pham}"
    
    class Meta:
        verbose_name = 'Hợp đồng bảo hiểm'
        verbose_name_plural = 'Hợp đồng bảo hiểm'
        db_table = 'hop_dong'
        ordering = ['-ngay_ky']