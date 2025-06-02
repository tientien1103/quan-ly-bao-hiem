from django.db import models
from .customer import KHACHHANG
from .product import LOAI_SANPHAM

class HOPDONG(models.Model):
    MA_HD = models.CharField(max_length=15, primary_key=True)
    MA_KH = models.ForeignKey(KHACHHANG, on_delete=models.CASCADE)
    MA_SP = models.ForeignKey(LOAI_SANPHAM, on_delete=models.CASCADE)
    MENH_GIA = models.DecimalField(max_digits=15, decimal_places=2)
    NGAY_BAT_DAU = models.DateField()
    NGAY_HET_HAN = models.DateField()
    PHI_CO_BAN = models.DecimalField(max_digits=15, decimal_places=2)
    CHIET_KHAU = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'HOPDONG'
        verbose_name = 'Hợp đồng'
        verbose_name_plural = 'Hợp đồng'