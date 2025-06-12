# core/management/commands/create_sample_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import random

from core.models import Address
from khachhang.models import KhachHang
from sanpham.models import SanPham
from hopdong.models import HopDong
from phi.models import BangPhiCoi, PhiQuanLy, PhiThanhToan
from thanhtoan.models import ThanhToan, CongNo

User = get_user_model()

class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho hệ thống bảo hiểm'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Xóa dữ liệu cũ trước khi tạo mới',
        )
    
    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Đang xóa dữ liệu cũ...')
            self.reset_data()
        
        self.stdout.write('Đang tạo dữ liệu mẫu...')
        
        # Tạo users
        admin_user, manager_user, agent_user, customer_users = self.create_users()
        
        # Tạo địa chỉ
        addresses = self.create_addresses(admin_user)
        
        # Tạo khách hàng
        khach_hangs = self.create_khach_hangs(agent_user, addresses, customer_users)
        
        # Tạo sản phẩm
        san_phams = self.create_san_phams(admin_user)
        
        # Tạo bảng phí
        self.create_bang_phi(admin_user, san_phams)
        
        # Tạo hợp đồng
        hop_dongs = self.create_hop_dongs(agent_user, khach_hangs, san_phams)
        
        # Tạo phí thanh toán
        phi_thanh_toans = self.create_phi_thanh_toan(admin_user, hop_dongs)
        
        # Tạo thanh toán và công nợ
        self.create_thanh_toan_cong_no(agent_user, hop_dongs, phi_thanh_toans)
        
        self.stdout.write(
            self.style.SUCCESS('Tạo dữ liệu mẫu thành công!')
        )
    
    def reset_data(self):
        """Xóa dữ liệu cũ"""
        ThanhToan.objects.all().delete()
        CongNo.objects.all().delete()
        PhiThanhToan.objects.all().delete()
        BangPhiCoi.objects.all().delete()
        PhiQuanLy.objects.all().delete()
        HopDong.objects.all().delete()
        SanPham.objects.all().delete()
        KhachHang.objects.all().delete()
        Address.objects.all().delete()
        User.objects.filter(username__in=['admin', 'manager', 'agent1', 'customer1', 'customer2', 'customer3']).delete()
    
    def create_users(self):
        """Tạo users mẫu"""
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@insurance.com',
                'phone': '0900000001',
                'first_name': 'Admin',
                'last_name': 'System',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
        
        manager_user, created = User.objects.get_or_create(
            username='manager',
            defaults={
                'email': 'manager@insurance.com',
                'phone': '0900000002',
                'first_name': 'Quản lý',
                'last_name': 'Hệ thống',
                'role': 'manager'
            }
        )
        if created:
            manager_user.set_password('manager123')
            manager_user.save()
        
        agent_user, created = User.objects.get_or_create(
            username='agent1',
            defaults={
                'email': 'agent1@insurance.com',
                'phone': '0900000003',
                'first_name': 'Nguyễn Văn',
                'last_name': 'Agent',
                'role': 'agent'
            }
        )
        if created:
            agent_user.set_password('agent123')
            agent_user.save()
        
        # Tạo customer users
        customer_users = []
        for i in range(1, 4):
            customer_user, created = User.objects.get_or_create(
                username=f'customer{i}',
                defaults={
                    'email': f'customer{i}@gmail.com',
                    'phone': f'090000000{i+3}',
                    'first_name': f'Khách hàng',
                    'last_name': f'Số {i}',
                    'role': 'customer'
                }
            )
            if created:
                customer_user.set_password('customer123')
                customer_user.save()
            customer_users.append(customer_user)
        
        return admin_user, manager_user, agent_user, customer_users
    
    def create_addresses(self, created_by):
        """Tạo địa chỉ mẫu"""
        addresses_data = [
            {
                'street': '123 Nguyễn Huệ',
                'ward': 'Phường Bến Nghé',
                'district': 'Quận 1',
                'city': 'TP. Hồ Chí Minh',
                'postal_code': '70000'
            },
            {
                'street': '456 Lê Lợi',
                'ward': 'Phường Phạm Ngũ Lão',
                'district': 'Quận 1',
                'city': 'TP. Hồ Chí Minh',
                'postal_code': '70000'
            },
            {
                'street': '789 Điện Biên Phủ',
                'ward': 'Phường 15',
                'district': 'Quận Bình Thạnh',
                'city': 'TP. Hồ Chí Minh',
                'postal_code': '70000'
            }
        ]
        
        addresses = []
        for addr_data in addresses_data:
            addr_data['created_by'] = created_by
            address = Address.objects.create(**addr_data)
            addresses.append(address)
        
        return addresses
    
    def create_khach_hangs(self, created_by, addresses, customer_users):
        """Tạo khách hàng mẫu"""
        khach_hangs_data = [
            {
                'ho_ten': 'Nguyễn Văn An',
                'ngay_sinh': date(1990, 5, 15),
                'gioi_tinh': 'nam',
                'so_cmnd': '123456789',
                'ngay_cap_cmnd': date(2010, 1, 1),
                'noi_cap_cmnd': 'CA TP.HCM',
                'so_dien_thoai': '0901234567',
                'email': 'nguyenvanan@gmail.com',
                'nghe_nghiep': 'Kỹ sư IT',
                'noi_lam_viec': 'Công ty ABC',
                'thu_nhap_hang_thang': Decimal('15000000'),
                'ten_nguoi_thu_huong': 'Nguyễn Thị Bình',
                'quan_he_nguoi_thu_huong': 'Vợ'
            },
            {
                'ho_ten': 'Trần Thị Bình',
                'ngay_sinh': date(1985, 8, 20),
                'gioi_tinh': 'nu',
                'so_cmnd': '987654321',
                'ngay_cap_cmnd': date(2008, 6, 15),
                'noi_cap_cmnd': 'CA TP.HCM',
                'so_dien_thoai': '0907654321',
                'email': 'tranthibinh@gmail.com',
                'nghe_nghiep': 'Giáo viên',
                'noi_lam_viec': 'Trường THPT XYZ',
                'thu_nhap_hang_thang': Decimal('8000000'),
                'ten_nguoi_thu_huong': 'Trần Văn Cường',
                'quan_he_nguoi_thu_huong': 'Con trai'
            },
            {
                'ho_ten': 'Lê Văn Cường',
                'ngay_sinh': date(1992, 12, 10),
                'gioi_tinh': 'nam',
                'so_cmnd': '456789123',
                'ngay_cap_cmnd': date(2012, 3, 20),
                'noi_cap_cmnd': 'CA TP.HCM',
                'so_dien_thoai': '0903456789',
                'email': 'levancuong@gmail.com',
                'nghe_nghiep': 'Bác sĩ',
                'noi_lam_viec': 'Bệnh viện 115',
                'thu_nhap_hang_thang': Decimal('20000000'),
                'ten_nguoi_thu_huong': 'Lê Thị Dung',
                'quan_he_nguoi_thu_huong': 'Mẹ'
            }
        ]
        
        khach_hangs = []
        for i, kh_data in enumerate(khach_hangs_data):
            kh_data['created_by'] = created_by
            kh_data['dia_chi'] = addresses[i]
            if i < len(customer_users):
                kh_data['user'] = customer_users[i]
            
            khach_hang = KhachHang.objects.create(**kh_data)
            khach_hangs.append(khach_hang)
        
        return khach_hangs
    
    def create_san_phams(self, created_by):
        """Tạo sản phẩm mẫu"""
        san_phams_data = [
            {
                'ten_san_pham': 'Bảo hiểm nhân thọ An Gia',
                'mo_ta': 'Sản phẩm bảo hiểm nhân thọ với quyền lợi toàn diện',
                'loai_san_pham': 'nhan_tho',
                'phi_bao_hiem_toi_thieu': Decimal('1000000'),
                'phi_bao_hiem_toi_da': Decimal('50000000'),
                'so_tien_bao_hiem_toi_thieu': Decimal('100000000'),
                'so_tien_bao_hiem_toi_da': Decimal('5000000000'),
                'thoi_han_toi_thieu': 12,
                'thoi_han_toi_da': 600,
                'tuoi_toi_thieu': 18,
                'tuoi_toi_da': 65,
                'ty_le_phi_quan_ly': Decimal('0.0500')
            },
            {
                'ten_san_pham': 'Bảo hiểm sức khỏe Toàn Diện',
                'mo_ta': 'Bảo hiểm y tế với quyền lợi điều trị toàn diện',
                'loai_san_pham': 'suc_khoe',
                'phi_bao_hiem_toi_thieu': Decimal('500000'),
                'phi_bao_hiem_toi_da': Decimal('20000000'),
                'so_tien_bao_hiem_toi_thieu': Decimal('50000000'),
                'so_tien_bao_hiem_toi_da': Decimal('2000000000'),
                'thoi_han_toi_thieu': 12,
                'thoi_han_toi_da': 120,
                'tuoi_toi_thieu': 0,
                'tuoi_toi_da': 70,
                'ty_le_phi_quan_ly': Decimal('0.0300')
            },
            {
                'ten_san_pham': 'Bảo hiểm xe ô tô Vững Chắc',
                'mo_ta': 'Bảo hiểm thiệt hại vật chất cho xe ô tô',
                'loai_san_pham': 'xe_co',
                'phi_bao_hiem_toi_thieu': Decimal('2000000'),
                'phi_bao_hiem_toi_da': Decimal('100000000'),
                'so_tien_bao_hiem_toi_thieu': Decimal('200000000'),
                'so_tien_bao_hiem_toi_da': Decimal('5000000000'),
                'thoi_han_toi_thieu': 12,
                'thoi_han_toi_da': 36,
                'tuoi_toi_thieu': 18,
                'tuoi_toi_da': 75,
                'ty_le_phi_quan_ly': Decimal('0.0200')
            }
        ]
        
        san_phams = []
        for sp_data in san_phams_data:
            sp_data['created_by'] = created_by
            san_pham = SanPham.objects.create(**sp_data)
            san_phams.append(san_pham)
        
        return san_phams
    
    def create_bang_phi(self, created_by, san_phams):
        """Tạo bảng phí coi và phí quản lý"""
        # Tạo bảng phí coi cho sản phẩm nhân thọ
        sp_nhan_tho = san_phams[0]
        bang_phi_data = [
            {
                'san_pham': sp_nhan_tho,
                'tuoi_tu': 18, 'tuoi_den': 30,
                'menh_gia_tu': Decimal('100000000'), 'menh_gia_den': Decimal('1000000000'),
                'ty_le_phi': Decimal('0.8000'), 'phi_co_dinh': Decimal('50000'),
                'created_by': created_by
            },
            {
                'san_pham': sp_nhan_tho,
                'tuoi_tu': 31, 'tuoi_den': 45,
                'menh_gia_tu': Decimal('100000000'), 'menh_gia_den': Decimal('1000000000'),
                'ty_le_phi': Decimal('1.2000'), 'phi_co_dinh': Decimal('80000'),
                'created_by': created_by
            },
            {
                'san_pham': sp_nhan_tho,
                'tuoi_tu': 46, 'tuoi_den': 65,
                'menh_gia_tu': Decimal('100000000'), 'menh_gia_den': Decimal('1000000000'),
                'ty_le_phi': Decimal('1.8000'), 'phi_co_dinh': Decimal('120000'),
                'created_by': created_by
            }
        ]
        
        for data in bang_phi_data:
            BangPhiCoi.objects.create(**data)
        
        # Tạo phí quản lý cho tất cả sản phẩm
        for san_pham in san_phams:
            PhiQuanLy.objects.create(
                san_pham=san_pham,
                ty_le_phi_quan_ly=san_pham.ty_le_phi_quan_ly,
                phi_quan_ly_toi_thieu=Decimal('10000'),
                phi_quan_ly_toi_da=Decimal('1000000'),
                created_by=created_by
            )
    
    def create_hop_dongs(self, created_by, khach_hangs, san_phams):
        """Tạo hợp đồng mẫu"""
        hop_dongs = []
        
        for i, khach_hang in enumerate(khach_hangs):
            san_pham = san_phams[i % len(san_phams)]
            
            hop_dong = HopDong.objects.create(
                khach_hang=khach_hang,
                san_pham=san_pham,
                nhan_vien_ban=created_by,
                ngay_ky=date.today() - timedelta(days=random.randint(30, 365)),
                ngay_hieu_luc=date.today() - timedelta(days=random.randint(1, 30)),
                ngay_ket_thuc=date.today() + timedelta(days=random.randint(365, 1095)),
                so_tien_bao_hiem=Decimal(str(random.randint(100, 1000))) * Decimal('1000000'),
                phi_bao_hiem=Decimal(str(random.randint(1, 10))) * Decimal('1000000'),
                ky_han_dong_phi='hang_thang',
                trang_thai='hoat_dong',
                ten_nguoi_thu_huong=khach_hang.ten_nguoi_thu_huong,
                quan_he_nguoi_thu_huong=khach_hang.quan_he_nguoi_thu_huong,
                created_by=created_by
            )
            hop_dongs.append(hop_dong)
        
        return hop_dongs
    
    def create_phi_thanh_toan(self, created_by, hop_dongs):
        """Tạo phí thanh toán mẫu"""
        phi_thanh_toans = []
        
        for hop_dong in hop_dongs:
            # Tạo phí cho 6 tháng gần đây
            for i in range(6):
                thang_nam = date.today().replace(day=1) - timedelta(days=i*30)
                
                phi_thanh_toan = PhiThanhToan.objects.create(
                    hop_dong=hop_dong,
                    thang_nam=thang_nam,
                    phi_bao_hiem=hop_dong.phi_bao_hiem,
                    phi_quan_ly=hop_dong.phi_bao_hiem * hop_dong.san_pham.ty_le_phi_quan_ly / 100,
                    phi_coi=Decimal('50000'),
                    ngay_dao_han=thang_nam + timedelta(days=15),
                    da_thanh_toan=random.choice([True, False]),
                    created_by=created_by
                )
                
                if phi_thanh_toan.da_thanh_toan:
                    phi_thanh_toan.ngay_thanh_toan = phi_thanh_toan.ngay_dao_han - timedelta(days=random.randint(1, 10))
                    phi_thanh_toan.save()
                
                phi_thanh_toans.append(phi_thanh_toan)
        
        return phi_thanh_toans
    
    def create_thanh_toan_cong_no(self, created_by, hop_dongs, phi_thanh_toans):
        """Tạo thanh toán và công nợ mẫu"""
        # Tạo thanh toán cho các phí đã thanh toán
        for phi in phi_thanh_toans:
            if phi.da_thanh_toan:
                ThanhToan.objects.create(
                    hop_dong=phi.hop_dong,
                    phi_thanh_toan=phi,
                    so_tien=phi.tong_phi,
                    phuong_thuc_thanh_toan=random.choice(['chuyen_khoan', 'tien_mat', 'the_tin_dung']),
                    trang_thai='thanh_cong',
                    nhan_vien_xu_ly=created_by,
                    created_by=created_by
                )
        
        # Tạo công nợ cho các phí chưa thanh toán
        for phi in phi_thanh_toans:
            if not phi.da_thanh_toan and phi.ngay_dao_han < date.today():
                CongNo.objects.create(
                    hop_dong=phi.hop_dong,
                    so_tien_no=phi.tong_phi,
                    ngay_phat_sinh=phi.ngay_dao_han,
                    ngay_dao_han=phi.ngay_dao_han + timedelta(days=30),
                    ty_le_phi_tre_han=Decimal('0.0500'),
                    created_by=created_by
                )