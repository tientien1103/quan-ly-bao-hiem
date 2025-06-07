# khachhang/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from core.permissions import KhachHangPermission, KhachHangDetailPermission
from .models import KhachHang
from .serializers import KhachHangSerializer, KhachHangCreateSerializer

class KhachHangListView(APIView):
    """API cho danh sách khách hàng"""
    permission_classes = [KhachHangPermission]
    
    def get(self, request):
        """GET /khachhang/ - Danh sách khách hàng"""
        # Phân quyền xem dữ liệu
        user_role = request.user.role
        
        if user_role == 'admin':
            queryset = KhachHang.objects.all()
        elif user_role == 'manager':
            queryset = KhachHang.objects.filter(is_active=True)
        elif user_role == 'agent':
            # Agent chỉ xem khách hàng của mình
            queryset = KhachHang.objects.filter(
                Q(created_by=request.user) | Q(user=request.user)
            )
        else:
            # Customer chỉ xem chính mình
            queryset = KhachHang.objects.filter(user=request.user)
        
        # Search functionality
        search = request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(ho_ten__icontains=search) |
                Q(so_dien_thoai__icontains=search) |
                Q(email__icontains=search) |
                Q(so_cmnd__icontains=search)
            )
        
        # Filter by status
        trang_thai = request.query_params.get('trang_thai', '')
        if trang_thai:
            queryset = queryset.filter(trang_thai=trang_thai)
        
        serializer = KhachHangSerializer(queryset, many=True)
        
        return Response({
            'message': 'Danh sách khách hàng',
            'user_role': user_role,
            'count': queryset.count(),
            'data': serializer.data
        })
    
    def post(self, request):
        """POST /khachhang/ - Tạo khách hàng mới"""
        serializer = KhachHangCreateSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            khach_hang = serializer.save()
            response_serializer = KhachHangSerializer(khach_hang)
            
            return Response({
                'message': 'Tạo khách hàng thành công',
                'user_role': request.user.role,
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'message': 'Dữ liệu không hợp lệ',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class KhachHangDetailView(APIView):
    """API cho chi tiết khách hàng"""
    permission_classes = [KhachHangDetailPermission]
    
    def get_object(self, ma_kh, user):
        """Lấy object với phân quyền"""
        try:
            khach_hang = KhachHang.objects.get(ma_kh=ma_kh)
            
            # Kiểm tra quyền xem
            if user.role in ['admin', 'manager']:
                return khach_hang
            elif user.role == 'agent':
                if khach_hang.created_by == user or khach_hang.user == user:
                    return khach_hang
            elif user.role == 'customer':
                if khach_hang.user == user:
                    return khach_hang
            
            return None
        except KhachHang.DoesNotExist:
            return None
    
    def get(self, request, ma_kh):
        """GET /khachhang/{ma_kh}/ - Chi tiết khách hàng"""
        khach_hang = self.get_object(ma_kh, request.user)
        
        if not khach_hang:
            return Response({
                'message': 'Không tìm thấy khách hàng hoặc không có quyền truy cập'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = KhachHangSerializer(khach_hang)
        
        return Response({
            'message': f'Chi tiết khách hàng {ma_kh}',
            'user_role': request.user.role,
            'data': serializer.data
        })
    
    def put(self, request, ma_kh):
        """PUT /khachhang/{ma_kh}/ - Cập nhật khách hàng"""
        khach_hang = self.get_object(ma_kh, request.user)
        
        if not khach_hang:
            return Response({
                'message': 'Không tìm thấy khách hàng hoặc không có quyền truy cập'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = KhachHangSerializer(khach_hang, data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': f'Cập nhật khách hàng {ma_kh} thành công',
                'user_role': request.user.role,
                'data': serializer.data
            })
        
        return Response({
            'message': 'Dữ liệu không hợp lệ',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, ma_kh):
        """PATCH /khachhang/{ma_kh}/ - Cập nhật một phần khách hàng"""
        khach_hang = self.get_object(ma_kh, request.user)
        
        if not khach_hang:
            return Response({
                'message': 'Không tìm thấy khách hàng hoặc không có quyền truy cập'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = KhachHangSerializer(khach_hang, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': f'Cập nhật một phần khách hàng {ma_kh} thành công',
                'user_role': request.user.role,
                'data': serializer.data
            })
        
        return Response({
            'message': 'Dữ liệu không hợp lệ',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, ma_kh):
        """DELETE /khachhang/{ma_kh}/ - Xóa khách hàng"""
        khach_hang = self.get_object(ma_kh, request.user)
        
        if not khach_hang:
            return Response({
                'message': 'Không tìm thấy khách hàng hoặc không có quyền truy cập'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Soft delete
        khach_hang.is_active = False
        khach_hang.trang_thai = 'khoa'
        khach_hang.save()
        
        return Response({
            'message': f'Xóa khách hàng {ma_kh} thành công',
            'user_role': request.user.role
        }, status=status.HTTP_204_NO_CONTENT)