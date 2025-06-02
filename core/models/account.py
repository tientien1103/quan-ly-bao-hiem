from django.db import models

class TAIKHOAN(models.Model):
    USERNAME = models.CharField(max_length=50, primary_key=True)
    MATKHAU = models.CharField(max_length=100)
    VAITRO = models.CharField(max_length=20, default='NHANVIEN')

    class Meta:
        db_table = 'TAIKHOAN'
        verbose_name = 'Tài khoản'
        verbose_name_plural = 'Tài khoản'