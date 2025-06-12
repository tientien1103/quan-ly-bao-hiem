# thanhtoan/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404
from core.permissions import ThanhToanPermission, ThanhToanDetailPermission
from .models import ThanhToan, CongNo
from .serializers import ThanhToanSerializer, CongNoSerializer
from hopdong.models import HopDong
from phi.models import PhiThanhToan

class ThanhToanListView(APIView):
    """API danh sách thanh toán"""
    permission_classes = [ThanhToanPermission]
    
    def get(self, request):
        """GET /thanh-toan/ - Danh sách thanh toán"""
        user_role = request.user.role
        
        # Phân quyền xem dữ liệu
        if user_role == 'admin':
            queryset = ThanhToan.objects.all()
        elif user_role == 'manager':
            queryset = ThanhToan.objects.filter(is_active=True)
        elif user_role == 'agent':
            # Agent xem thanh toán của hợp đồng mình phụ trách
            queryset = ThanhToan.objects.filter(
                Q(hop_dong__nhan_vien_ban=request.user) |
                Q(hop_dong__created_by=request.user) |
                Q(nhan_vien_xu_ly=request.user)
            )
        else:
            return Response({
                'message': 'Không có quyền xem danh sách thanh toán'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Search functionality
        search = request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(ma_thanh_toan__icontains=search) |
                Q(hop_dong__ma_hd__icontains=search) |
                Q(hop_dong__khach_hang__ho_ten__icontains=search)
            )
        
        # Filter by trang_thai
        trang_thai = request.query_params.get('trang_thai', '')
        if trang_thai:
            queryset = queryset.filter(trang_thai=trang_thai)
        
        # Filter by phuong_thuc_thanh_toan
        phuong_thuc = request.query_params.get('phuong_thuc', '')
        if phuong_thuc:
            queryset = queryset.filter(phuong_thuc_thanh_toan=phuong_thuc)
        
        # Filter by date range
        tu_ngay = request.query_params.get('tu_ngay', '')
        den_ngay = request.query_params.get('den_ngay', '')
        if tu_ngay:
            queryset = queryset.filter(ngay_thanh_toan__date__gte=tu_ngay)
        if den_ngay:
            queryset = queryset.filter(ngay_thanh_toan__date__lte=den_ngay)
        
        # Order by latest
        queryset = queryset.order_by('-ngay_thanh_toan')
        
        # Calculate summary
        tong_so_tien = queryset.aggregate(tong=Sum('so_tien'))['tong'] or 0
        
        serializer = ThanhToanSerializer(queryset, many=True)
        
        return Response({
            'message': 'Danh sách thanh toán',
            'user_role': user_role,
            'thong_ke': {
                'tong_giao_dich': queryset.count(),
                'tong_so_tien': float(tong_so_tien)
            },
            'data': serializer.data
        })
    
    def post(self, request):
        """POST /thanh-toan/ - Tạo thanh toán mới"""
        serializer = ThanhToanSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            thanh_toan = serializer.save()
            return Response({
                'message': 'Tạo thanh toán thành công',
                'user_role': request.user.role,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'message': 'Dữ liệu không hợp lệ',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ThanhToanDetailView(APIView):
    """API chi tiết thanh toán"""
    permission_classes = [ThanhToanDetailPermission]
    
    def get(self, request, ma_hd):
        """GET /thanh-toan/{ma_hd}/ - Chi tiết thanh toán theo hợp đồng"""
        try:
            hop_dong = HopDong.objects.get(ma_hd=ma_hd)
            
            # Kiểm tra quyền truy cập
            if not self._check_permission(hop_dong, request.user):
                return Response({
                    'message': 'Không có quyền truy cập hợp đồng này'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Lấy danh sách thanh toán
            thanh_toan_list = ThanhToan.objects.filter(
                hop_dong=hop_dong
            ).order_by('-ngay_thanh_toan')
            
            # Tính tổng đã thanh toán
            tong_da_thanh_toan = thanh_toan_list.filter(
                trang_thai='thanh_cong'
            ).aggregate(tong=Sum('so_tien'))['tong'] or 0
            
            serializer = ThanhToanSerializer(thanh_toan_list, many=True)
            
            return Response({
                'message': f'Chi tiết thanh toán cho hợp đồng {ma_hd}',
                'user_role': request.user.role,
                'hop_dong_info': {
                    'ma_hd': hop_dong.ma_hd,
                    'khach_hang': hop_dong.khach_hang.ho_ten,
                    'san_pham': hop_dong.san_pham.ten_san_pham,
                    'so_tien_bao_hiem': float(hop_dong.so_tien_bao_hiem),
                    'phi_bao_hiem': float(hop_dong.phi_bao_hiem)
                },
                'thong_ke_thanh_toan': {
                    'tong_giao_dich': thanh_toan_list.count(),
                    'tong_da_thanh_toan': float(tong_da_thanh_toan),
                    'phi_bao_hiem_hang_ky': float(hop_dong.phi_bao_hiem)
                },
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

class ConNoView(APIView):
    """API công nợ"""
    permission_classes = [ThanhToanDetailPermission]
    
    def get(self, request, ma_hd):
        """GET /thanh-toan/con-no/{ma_hd}/ - Công nợ theo hợp đồng"""
        try:
            hop_dong = HopDong.objects.get(ma_hd=ma_hd)
            
            # Kiểm tra quyền truy cập
            if not self._check_permission(hop_dong, request.user):
                return Response({
                    'message': 'Không có quyền truy cập hợp đồng này'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Lấy danh sách công nợ
            cong_no_list = CongNo.objects.filter(
                hop_dong=hop_dong
            ).order_by('-ngay_phat_sinh')
            
            # Tính tổng công nợ
            tong_cong_no = sum(cn.tong_cong_no for cn in cong_no_list if not cn.da_thanh_toan)
            cong_no_qua_han = sum(cn.tong_cong_no for cn in cong_no_list if not cn.da_thanh_toan and cn.so_ngay_tre_han > 0)
            
            serializer = CongNoSerializer(cong_no_list, many=True)
            
            return Response({
                'message': f'Công nợ cho hợp đồng {ma_hd}',
                'user_role': request.user.role,
                'hop_dong_info': {
                    'ma_hd': hop_dong.ma_hd,
                    'khach_hang': hop_dong.khach_hang.ho_ten,
                    'san_pham': hop_dong.san_pham.ten_san_pham
                },
                'thong_ke_cong_no': {
                    'tong_ban_ghi': cong_no_list.count(),
                    'tong_cong_no': float(tong_cong_no),
                    'cong_no_qua_han': float(cong_no_qua_han),
                    'so_ban_ghi_qua_han': len([cn for cn in cong_no_list if not cn.da_thanh_toan and cn.so_ngay_tre_han > 0])
                },
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