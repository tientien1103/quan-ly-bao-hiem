# Generated by Django 5.2.2 on 2025-06-07 09:54

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('khachhang', '0001_initial'),
        ('sanpham', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HopDong',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')),
                ('is_active', models.BooleanField(default=True, verbose_name='Kích hoạt')),
                ('ma_hd', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='Mã hợp đồng')),
                ('ngay_ky', models.DateField(default=datetime.date.today, verbose_name='Ngày ký')),
                ('ngay_hieu_luc', models.DateField(verbose_name='Ngày hiệu lực')),
                ('ngay_ket_thuc', models.DateField(verbose_name='Ngày kết thúc')),
                ('so_tien_bao_hiem', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Số tiền bảo hiểm')),
                ('phi_bao_hiem', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Phí bảo hiểm')),
                ('ky_han_dong_phi', models.CharField(choices=[('hang_thang', 'Hàng tháng'), ('hang_quy', 'Hàng quý'), ('hang_nam', 'Hàng năm'), ('mot_lan', 'Một lần')], default='hang_thang', max_length=20, verbose_name='Kỳ hạn đóng phí')),
                ('trang_thai', models.CharField(choices=[('cho_duyet', 'Chờ duyệt'), ('hoat_dong', 'Hoạt động'), ('tam_dung', 'Tạm dừng'), ('het_han', 'Hết hạn'), ('huy_bo', 'Hủy bỏ')], default='cho_duyet', max_length=20, verbose_name='Trạng thái')),
                ('ten_nguoi_thu_huong', models.CharField(max_length=100, verbose_name='Tên người thụ hưởng')),
                ('quan_he_nguoi_thu_huong', models.CharField(max_length=50, verbose_name='Quan hệ với người thụ hưởng')),
                ('ghi_chu', models.TextField(blank=True, verbose_name='Ghi chú')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Người tạo')),
                ('khach_hang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hop_dong_list', to='khachhang.khachhang', verbose_name='Khách hàng')),
                ('nhan_vien_ban', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hop_dong_ban', to=settings.AUTH_USER_MODEL, verbose_name='Nhân viên bán')),
                ('san_pham', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hop_dong_list', to='sanpham.sanpham', verbose_name='Sản phẩm')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Người cập nhật')),
            ],
            options={
                'verbose_name': 'Hợp đồng bảo hiểm',
                'verbose_name_plural': 'Hợp đồng bảo hiểm',
                'db_table': 'hop_dong',
                'ordering': ['-ngay_ky'],
            },
        ),
    ]
