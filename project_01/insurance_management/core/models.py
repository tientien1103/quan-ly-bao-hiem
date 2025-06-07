from django.db import models
from django.conf import settings
import uuid

class BaseModel(models.Model):
    """Abstract base model với các trường chung"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created',
        verbose_name='Người tạo'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated',
        verbose_name='Người cập nhật'
    )
    is_active = models.BooleanField(default=True, verbose_name='Kích hoạt')

    class Meta:
        abstract = True

class Address(BaseModel):
    """Model địa chỉ"""
    street = models.CharField(max_length=255, verbose_name='Địa chỉ')
    ward = models.CharField(max_length=100, verbose_name='Phường/Xã')
    district = models.CharField(max_length=100, verbose_name='Quận/Huyện')
    city = models.CharField(max_length=100, verbose_name='Tỉnh/Thành phố')
    country = models.CharField(max_length=100, default='Vietnam', verbose_name='Quốc gia')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='Mã bưu điện')

    def __str__(self):
        return f"{self.street}, {self.ward}, {self.district}, {self.city}"

    class Meta:
        verbose_name = 'Địa chỉ'
        verbose_name_plural = 'Địa chỉ'
        db_table = 'core_address'