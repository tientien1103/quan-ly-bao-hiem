# hopdong/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import datetime, date
from core.permissions import HopDongPermission
from .models import HopDong
from .serializers import HopDongSerializer, TinhPhiHopDongSerializer

class HopDongListView(APIView):
    """API cho danh sách hợp đồng"""
    permission_classes = [HopDongPermission]
    
    def get(self, request):
        """GET /hopdong/ - Danh sách hợp đồng"""
        user_role = request.user.role
        
        # Phân quyền xem dữ liệu
        if user_role == 'admin':
            queryset = HopDong.objects.all()
        elif user_role == 'manager':
            queryset = HopDong.objects.filter(is_active=True)
        elif user_role == 'agent':
            # Agent xem hợp đồng của khách hàng mình phụ trách hoặc do mình bán
            queryset = HopDong.objects.filter(
                Q(nhan_vien_ban=request.user) | 
                Q(khach_hang__created_by=request.user) |
                Q(created_by=request.user)
            )
        else:
            # Customer chỉ xem hợp đồng của mình
            queryset = HopDong.objects.filter(khach_hang__user=request.user)
        
        # Search functionality
        search = request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(ma_hd__icontains=search) |
                Q(khach_hang__ho_ten__icontains=search) |
                Q(san_pham__ten_san_pham__icontains=search)
            )
        
        # Filter by trang_thai
        trang_thai = request.query_params.get('trang_thai', '')
        if trang_thai:
            queryset = queryset.filter(trang_thai=trang_thai)
        
        # Filter by san_pham
        ma_sp = request.query_params.get('ma_sp', '')
        if ma_sp:
            queryset = queryset.filter(san_pham__ma_sp=ma_sp)
        
        # Filter by khach_hang
        ma_kh = request.query_params.get('ma_kh', '')
        if ma_kh:
            queryset = queryset.filter(khach_hang__ma_kh=ma_kh)
        
        # Order by latest
        queryset = queryset.order_by('-ngay_ky')
        
        serializer = HopDongSerializer(queryset, many=True)
        
        return Response({
            'message': 'Danh sách hợp đồng',
            'user_role': user_role,
            'count': queryset.count(),
            'data': serializer.data
        })
    
    def post(self, request):
        """POST /hopdong/ - Tạo hợp đồng mới"""
        serializer = HopDongSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            hop_dong = serializer.save()
            return Response({
                'message': 'Tạo hợp đồng thành công',
                'user_role': request.user.role,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'message': 'Dữ liệu không hợp lệ',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class HopDongDetailView(APIView):
    """API cho chi tiết hợp đồng"""
    permission_classes = [HopDongPermission]
    
    def get_object(self, ma_hd, user):
        """Lấy object với phân quyền"""
        try:
            hop_dong = HopDong.objects.get(ma_hd=ma_hd)
            
            # Kiểm tra quyền xem
            if user.role in ['admin', 'manager']:
                return hop_dong
            elif user.role == 'agent':
                if (hop_dong.nhan_vien_ban == user or 
                    hop_dong.khach_hang.created_by == user or 
                    hop_dong.created_by == user):
                    return hop_dong
            elif user.role == 'customer':
                if hop_dong.khach_hang.user == user:
                    return hop_dong
            
            return None
        except HopDong.DoesNotExist:
            return None
    
    def get(self, request, ma_hd):
        """GET /hopdong/{ma_hd}/ - Chi tiết hợp đồng"""
        hop_dong = self.get_object(ma_hd, request.user)
        
        if not hop_dong:
            return Response({
                'message': 'Không tìm thấy hợp đồng hoặc không có quyền truy cập'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = HopDongSerializer(hop_dong)
        
        return Response({
            'message': f'Chi tiết hợp đồng {ma_hd}',
            'user_role': request.user.role,
            'data': serializer.data
        })
    
    def put(self, request, ma_hd):
        """PUT /hopdong/{ma_hd}/ - Cập nhật hợp đồng"""
        hop_dong = self.get_object(ma_hd, request.user)
        
        if not hop_dong:
            return Response({
                'message': 'Không tìm thấy hợp đồng hoặc không có quyền truy cập'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Chỉ admin/manager mới được cập nhật
        if request.user.role not in ['admin', 'manager']:
            return Response({
                'message': 'Không có quyền cập nhật hợp đồng'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = HopDongSerializer(hop_dong, data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': f'Cập nhật hợp đồng {ma_hd} thành công',
                'user_role': request.user.role,
                'data': serializer.data
            })
        
        return Response({
            'message': 'Dữ liệu không hợp lệ',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, ma_hd):
        """PATCH /hopdong/{ma_hd}/ - Cập nhật một phần hợp đồng"""
        hop_dong = self.get_object(ma_hd, request.user)
        
        if not hop_dong:
            return Response({
                'message': 'Không tìm thấy hợp đồng hoặc không có quyền truy cập'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Chỉ admin/manager mới được cập nhật
        if request.user.role not in ['admin', 'manager']:
            return Response({
                'message': 'Không có quyền cập nhật hợp đồng'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = HopDongSerializer(hop_dong, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': f'Cập nhật một phần hợp đồng {ma_hd} thành công',
                'user_role': request.user.role,
                'data': serializer.data
            })
        
        return Response({
            'message': 'Dữ liệu không hợp lệ',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, ma_hd):
        """DELETE /hopdong/{ma_hd}/ - Xóa hợp đồng"""
        hop_dong = self.get_object(ma_hd, request.user)
        
        if not hop_dong:
            return Response({
                'message': 'Không tìm thấy hợp đồng hoặc không có quyền truy cập'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Chỉ admin mới được xóa
        if request.user.role != 'admin':
            return Response({
                'message': 'Không có quyền xóa hợp đồng'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Soft delete
        hop_dong.is_active = False
        hop_dong.trang_thai = 'huy_bo'
        hop_dong.save()
        
        return Response({
            'message': f'Xóa hợp đồng {ma_hd} thành công',
            'user_role': request.user.role
        }, status=status.HTTP_204_NO_CONTENT)

class HopDongTinhPhiView(APIView):
    """API tính phí hợp đồng"""
    permission_classes = [HopDongPermission]
    
    def get(self, request, ma_hd):
        """GET /hopdong/{ma_hd}/tinh-phi?thang_nam=YYYY-MM"""
        try:
            hop_dong = HopDong.objects.get(ma_hd=ma_hd)
            
            # Kiểm tra quyền xem
            if not self._check_permission(hop_dong, request.user):
                return Response({
                    'message': 'Không có quyền truy cập hợp đồng này'
                }, status=status.HTTP_403_FORBIDDEN)
            
            thang_nam_str = request.query_params.get('thang_nam')
            
            if not thang_nam_str:
                return Response({
                    'message': 'Vui lòng cung cấp tham số thang_nam (YYYY-MM)'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                thang_nam = datetime.strptime(thang_nam_str, '%Y-%m').date()
            except ValueError:
                return Response({
                    'message': 'Định dạng thang_nam không hợp lệ. Sử dụng YYYY-MM'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Tính phí cho tháng này
            phi_hang_thang = hop_dong.tinh_phi_hang_thang(thang_nam)
            
            # Lấy thông tin phí từ sản phẩm
            san_pham = hop_dong.san_pham
            phi_quan_ly = san_pham.ty_le_phi_quan_ly * phi_hang_thang / 100
            
            # Tính phí coi nếu có
            phi_coi = 0
            try:
                from phi.models import BangPhiCoi
                bang_phi_coi = BangPhiCoi.objects.filter(
                    san_pham=san_pham,
                    tuoi_tu__lte=hop_dong.khach_hang.tuoi,
                    tuoi_den__gte=hop_dong.khach_hang.tuoi,
                    menh_gia_tu__lte=hop_dong.so_tien_bao_hiem,
                    menh_gia_den__gte=hop_dong.so_tien_bao_hiem
                ).first()
                
                if bang_phi_coi:
                    phi_coi = bang_phi_coi.tinh_phi(hop_dong.so_tien_bao_hiem)
            except:
                pass
            
            tong_phi = phi_hang_thang + phi_quan_ly + phi_coi
            
            return Response({
                'message': f'Tính phí cho hợp đồng {ma_hd}',
                'user_role': request.user.role,
                'ma_hd': ma_hd,
                'thang_nam': thang_nam_str,
                'chi_tiet_phi': {
                    'phi_bao_hiem': float(phi_hang_thang),
                    'phi_quan_ly': float(phi_quan_ly),
                    'phi_coi': float(phi_coi),
                    'tong_phi': float(tong_phi)
                },
                'hop_dong_info': {
                    'khach_hang': hop_dong.khach_hang.ho_ten,
                    'san_pham': hop_dong.san_pham.ten_san_pham,
                    'so_tien_bao_hiem': float(hop_dong.so_tien_bao_hiem),
                    'ky_han_dong_phi': hop_dong.get_ky_han_dong_phi_display()
                }
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