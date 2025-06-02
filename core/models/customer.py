from django.db import models

class KHACHHANG(models.Model):
    MA_KH = models.CharField(max_length=10, primary_key=True)
    HO_TEN = models.CharField(max_length=100)
    NGAY_SINH = models.DateField()
    GIOI_TINH = models.CharField(max_length=1)
    DIEN_THOAI = models.CharField(max_length=20, blank=True, null=True)
    DIA_CHI = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'KHACHHANG'
        verbose_name = 'Khách hàng'
        verbose_name_plural = 'Khách hàng'