# Generated by Django 5.2.2 on 2025-06-07 09:54

import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SanPham',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')),
                ('is_active', models.BooleanField(default=True, verbose_name='Kích hoạt')),
                ('ma_sp', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='Mã sản phẩm')),
                ('ten_san_pham', models.CharField(max_length=200, verbose_name='Tên sản phẩm')),
                ('mo_ta', models.TextField(verbose_name='Mô tả')),
                ('loai_san_pham', models.CharField(choices=[('nhan_tho', 'Bảo hiểm nhân thọ'), ('suc_khoe', 'Bảo hiểm sức khỏe'), ('xe_co', 'Bảo hiểm xe cơ giới'), ('nha_o', 'Bảo hiểm nhà ở'), ('du_lich', 'Bảo hiểm du lịch'), ('doanh_nghiep', 'Bảo hiểm doanh nghiệp')], max_length=20, verbose_name='Loại sản phẩm')),
                ('phi_bao_hiem_toi_thieu', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Phí bảo hiểm tối thiểu')),
                ('phi_bao_hiem_toi_da', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Phí bảo hiểm tối đa')),
                ('so_tien_bao_hiem_toi_thieu', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Số tiền bảo hiểm tối thiểu')),
                ('so_tien_bao_hiem_toi_da', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Số tiền bảo hiểm tối đa')),
                ('thoi_han_toi_thieu', models.IntegerField(verbose_name='Thời hạn tối thiểu (tháng)')),
                ('thoi_han_toi_da', models.IntegerField(verbose_name='Thời hạn tối đa (tháng)')),
                ('tuoi_toi_thieu', models.IntegerField(verbose_name='Tuổi tối thiểu')),
                ('tuoi_toi_da', models.IntegerField(verbose_name='Tuổi tối đa')),
                ('ty_le_phi_quan_ly', models.DecimalField(decimal_places=4, default=Decimal('0.0500'), max_digits=5, verbose_name='Tỷ lệ phí quản lý (%)')),
                ('trang_thai', models.CharField(choices=[('hoat_dong', 'Hoạt động'), ('tam_dung', 'Tạm dừng'), ('ngung_ban', 'Ngừng bán')], default='hoat_dong', max_length=20, verbose_name='Trạng thái')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Người tạo')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Người cập nhật')),
            ],
            options={
                'verbose_name': 'Sản phẩm bảo hiểm',
                'verbose_name_plural': 'Sản phẩm bảo hiểm',
                'db_table': 'san_pham',
                'ordering': ['ten_san_pham'],
            },
        ),
    ]
