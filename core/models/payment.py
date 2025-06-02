from django.db import models
from .contract import HOPDONG

class PHI_THANHTOAN(models.Model):
    MA_HD = models.ForeignKey(HOPDONG, on_delete=models.CASCADE)
    THANG_NAM = models.CharField(max_length=7)
    TONG_PHI = models.DecimalField(max_digits=15, decimal_places=2)
    DA_THANH_TOAN = models.CharField(max_length=1, default='N')

    class Meta:
        db_table = 'PHI_THANHTOAN'
        unique_together = (('MA_HD', 'THANG_NAM'),)
        verbose_name = 'Phí thanh toán'
        verbose_name_plural = 'Phí thanh toán'

class LICHSU_THANHTOAN(models.Model):
    ID = models.CharField(max_length=20, primary_key=True)
    MA_HD = models.ForeignKey(HOPDONG, on_delete=models.CASCADE)
    NGAY_THANH_TOAN = models.DateField()
    SO_TIEN = models.DecimalField(max_digits=15, decimal_places=2)
    THANG_NAM = models.CharField(max_length=7)

    class Meta:
        db_table = 'LICHSU_THANHTOAN'
        verbose_name = 'Lịch sử thanh toán'
        verbose_name_plural = 'Lịch sử thanh toán'