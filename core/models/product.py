from django.db import models

class LOAI_SANPHAM(models.Model):
    MA_SP = models.CharField(max_length=10, primary_key=True)
    TEN_SP = models.CharField(max_length=100)
    MO_TA = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'LOAI_SANPHAM'
        verbose_name = 'Loại sản phẩm'
        verbose_name_plural = 'Loại sản phẩm'

class PHI_COI(models.Model):
    MA_SP = models.ForeignKey(LOAI_SANPHAM, on_delete=models.CASCADE)
    TUOI = models.SmallIntegerField()
    MENH_GIA = models.DecimalField(max_digits=15, decimal_places=2)
    PHI = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'PHI_COI'
        unique_together = (('MA_SP', 'TUOI', 'MENH_GIA'),)
        verbose_name = 'Phí COI'
        verbose_name_plural = 'Phí COI'

class PHI_QUANLY(models.Model):
    MA_SP = models.OneToOneField(LOAI_SANPHAM, on_delete=models.CASCADE, primary_key=True)
    PHI = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'PHI_QUANLY'
        verbose_name = 'Phí quản lý'
        verbose_name_plural = 'Phí quản lý'