# phi/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from core.permissions import PhiPermission
from .models import BangPhiCoi, PhiQuanLy, PhiThanhToan
from .serializers import (
    BangPhiCoiSerializer, 
    PhiQuanLySerializer, 
    PhiThanhToanSerializer,
    TinhPhiCoiSerializer
)
from sanpham.models import SanPham
from hopdong.models import HopDong

class PhiCoiView(APIView):
    """API tính phí coi"""
    permission_classes = [PhiPermission]
    
    def get(self, request):
        """GET /phi-coi?ma_sp=...&tuoi=...&menh_gia=..."""
        ma_sp = request.query_params.get('ma_sp')
        tuoi = request.query_params.get('tuoi')
        menh_gia = request.query_params.get('menh_gia')
        
        if not all([ma_sp, tuoi, menh_gia]):
            return Response({
                'message': 'Vui lòng cung cấp đầy đủ: ma_sp, tuoi, menh_gia'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            tuoi = int(tuoi)
            menh_gia = float(menh_gia)
        except ValueError:
            return Response({
                'message': 'Tuổi và mệnh giá phải là số'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            san_pham = SanPham.objects.get(ma_sp=ma_sp)
        except SanPham.DoesNotExist:
            return Response({
                'message': 'Không tìm thấy sản phẩm'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Kiểm tra tuổi có phù hợp với sản phẩm
        if tuoi < san_pham.tuoi_toi_thieu or tuoi > san_pham.tuoi_toi_da:
            return Response({
                'message': f'Tuổi không phù hợp với sản phẩm (yêu cầu: {san_pham.tuoi_toi_thieu}-{san_pham.tuoi_toi_da} tuổi)'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Tìm bảng phí coi phù hợp
        bang_phi_coi = BangPhiCoi.objects.filter(
            san_pham=san_pham,
            tuoi_tu__lte=tuoi,
            tuoi_den__gte=tuoi,
            menh_gia_tu__lte=menh_gia,
            menh_gia_den__gte=menh_gia,
            is_active=True
        ).first()
        
        if not bang_phi_coi:
            # Sử dụng công thức tính phí cơ bản của sản phẩm
            phi_coi = san_pham.tinh_phi_co_ban(tuoi, menh_gia)
            phuong_thuc = 'Công thức cơ bản'
        else:
            phi_coi = bang_phi_coi.tinh_phi(menh_gia)
            phuong_thuc = f'Bảng phí coi {bang_phi_coi.ma_phi_coi}'
        
        return Response({
            'message': 'Tính phí coi thành công',
            'user_role': request.user.role,
            'thong_tin_dau_vao': {
                'ma_sp': ma_sp,
                'ten_san_pham': san_pham.ten_san_pham,
                'tuoi': tuoi,
                'menh_gia': menh_gia
            },
            'ket_qua': {
                'phi_coi': float(phi_coi),
                'phuong_thuc_tinh': phuong_thuc,
                'ty_le_phi': float(bang_phi_coi.ty_le_phi) if bang_phi_coi else None
            }
        })
    
    def post(self, request):
        """POST /phi-coi - Tạo bảng phí coi mới"""
        serializer = BangPhiCoiSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            bang_phi_coi = serializer.save()
            return Response({
                'message': 'Tạo bảng phí coi thành công',
                'user_role': request.user.role,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'message': 'Dữ liệu không hợp lệ',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PhiQuanLyView(APIView):
    """API phí quản lý"""
    permission_classes = [PhiPermission]
    
    def get(self, request, ma_sp):
        """GET /phi-quan-ly/{ma_sp}/"""
        try:
            san_pham = SanPham.objects.get(ma_sp=ma_sp)
        except SanPham.DoesNotExist:
            return Response({
                'message': 'Không tìm thấy sản phẩm'
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            phi_quan_ly = PhiQuanLy.objects.get(san_pham=san_pham)
            serializer = PhiQuanLySerializer(phi_quan_ly)
            
            return Response({
                'message': f'Phí quản lý cho sản phẩm {ma_sp}',
                'user_role': request.user.role,
                'data': serializer.data
            })
        except PhiQuanLy.DoesNotExist:
            # Sử dụng tỷ lệ phí quản lý mặc định từ sản phẩm
            return Response({
                'message': f'Phí quản lý cho sản phẩm {ma_sp}',
                'user_role': request.user.role,
                'data': {
                    'san_pham': san_pham.ten_san_pham,
                    'ty_le_phi_quan_ly': float(san_pham.ty_le_phi_quan_ly),
                    'ghi_chu': 'Sử dụng tỷ lệ mặc định từ sản phẩm'
                }
            })

class PhiThanhToanView(APIView):
    """API phí thanh toán"""
    permission_classes = [PhiPermission]
    
    def get(self, request, ma_hd):
        """GET /phi-thanhtoan/{ma_hd}/"""
        try:
            hop_dong = HopDong.objects.get(ma_hd=ma_hd)
            
            # Kiểm tra quyền truy cập
            if not self._check_permission(hop_dong, request.user):
                return Response({
                    'message': 'Không có quyền truy cập hợp đồng này'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Lấy danh sách phí thanh toán
            phi_thanh_toan_list = PhiThanhToan.objects.filter(
                hop_dong=hop_dong
            ).order_by('-thang_nam')
            
            serializer = PhiThanhToanSerializer(phi_thanh_toan_list, many=True)
            
            return Response({
                'message': f'Phí thanh toán cho hợp đồng {ma_hd}',
                'user_role': request.user.role,
                'hop_dong_info': {
                    'ma_hd': hop_dong.ma_hd,
                    'khach_hang': hop_dong.khach_hang.ho_ten,
                    'san_pham': hop_dong.san_pham.ten_san_pham
                },
                'count': phi_thanh_toan_list.count(),
                'data': serializer.data
            })
            
        except HopDong.DoesNotExist:
            return Response({
                'message': 'Không tìm thấy hợp đồng'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def _check_permission(self, hop_dong, user):
        """Kiểm tra quyền truy cập hợp đồng"""
        if user.role in ['admin', 'manager']:
            return True
        elif user.role == 'agent':
            return (hop_dong.nhan_vien_ban == user or 
                   hop_dong.khach_hang.created_by == user or 
                   hop_dong.created_by == user)
        elif user.role == 'customer':
            return hop_dong.khach_hang.user == user
        return False

class TaoPhiThanhToanView(APIView):
    """API tạo phí thanh toán"""
    permission_classes = [PhiPermission]
    
    def post(self, request):
        """POST /phi-thanhtoan/tao-moi/"""
        serializer = PhiThanhToanSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            phi_thanh_toan = serializer.save()
            return Response({
                'message': 'Tạo phí thanh toán thành công',
                'user_role': request.user.role,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'message': 'Dữ liệu không hợp lệ',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)