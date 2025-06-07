from django.db import models
from django.contrib.auth import get_user_model
from core.models import BaseModel, Address
import uuid

User = get_user_model()

class GioiTinh(models.TextChoices):
    NAM = 'nam', 'Nam'
    NU = 'nu', 'Nữ'
    KHAC = 'khac', 'Khác'

class TrangThaiKhachHang(models.TextChoices):
    HOAT_DONG = 'hoat_dong', 'Hoạt động'
    TAM_DUNG = 'tam_dung', 'Tạm dừng'
    KHOA = 'khoa', 'Khóa'

class KhachHang(BaseModel):
    """Model khách hàng"""
    ma_kh = models.CharField(
        max_length=20, 
        unique=True, 
        primary_key=True,
        verbose_name='Mã khách hàng'
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='khach_hang',
        verbose_name='Tài khoản người dùng'
    )
    
    # Thông tin cá nhân
    ho_ten = models.CharField(max_length=100, verbose_name='Họ và tên')
    ngay_sinh = models.DateField(verbose_name='Ngày sinh')
    gioi_tinh = models.CharField(
        max_length=10,
        choices=GioiTinh.choices,
        default=GioiTinh.NAM,
        verbose_name='Giới tính'
    )
    so_cmnd = models.CharField(max_length=20, unique=True, verbose_name='Số CMND/CCCD')
    ngay_cap_cmnd = models.DateField(verbose_name='Ngày cấp CMND/CCCD')
    noi_cap_cmnd = models.CharField(max_length=100, verbose_name='Nơi cấp CMND/CCCD')
    
    # Thông tin liên hệ
    so_dien_thoai = models.CharField(max_length=20, verbose_name='Số điện thoại')
    email = models.EmailField(verbose_name='Email')
    dia_chi = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Địa chỉ'
    )
    
    # Thông tin nghề nghiệp
    nghe_nghiep = models.CharField(max_length=100, blank=True, verbose_name='Nghề nghiệp')
    noi_lam_viec = models.CharField(max_length=200, blank=True, verbose_name='Nơi làm việc')
    thu_nhap_hang_thang = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Thu nhập hàng tháng'
    )
    
    # Thông tin bảo hiểm
    trang_thai = models.CharField(
        max_length=20,
        choices=TrangThaiKhachHang.choices,
        default=TrangThaiKhachHang.HOAT_DONG,
        verbose_name='Trạng thái'
    )
    ngay_dang_ky = models.DateTimeField(auto_now_add=True, verbose_name='Ngày đăng ký')
    
    # Thông tin người thụ hưởng
    ten_nguoi_thu_huong = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Tên người thụ hưởng'
    )
    quan_he_nguoi_thu_huong = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Quan hệ với người thụ hưởng'
    )
    
    def save(self, *args, **kwargs):
        if not self.ma_kh:
            # Tự động tạo mã khách hàng
            self.ma_kh = f"KH{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def tuoi(self):
        """Tính tuổi khách hàng"""
        from datetime import date
        today = date.today()
        return today.year - self.ngay_sinh.year - (
            (today.month, today.day) < (self.ngay_sinh.month, self.ngay_sinh.day)
        )
    
    def __str__(self):
        return f"{self.ma_kh} - {self.ho_ten}"
    
    class Meta:
        verbose_name = 'Khách hàng'
        verbose_name_plural = 'Khách hàng'
        db_table = 'khach_hang'
        ordering = ['-ngay_dang_ky']