# sanpham/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from core.permissions import SanPhamPermission
from .models import SanPham
from .serializers import SanPhamSerializer, SanPhamTinhPhiSerializer

class SanPhamListView(APIView):
    """API cho danh sách sản phẩm"""
    permission_classes = [SanPhamPermission]
    
    def get(self, request):
        """GET /sanpham/ - Danh sách sản phẩm"""
        queryset = SanPham.objects.filter(is_active=True)
        
        # Search functionality
        search = request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(ten_san_pham__icontains=search) |
                Q(mo_ta__icontains=search)
            )
        
        # Filter by loai_san_pham
        loai = request.query_params.get('loai', '')
        if loai:
            queryset = queryset.filter(loai_san_pham=loai)
        
        # Filter by trang_thai
        trang_thai = request.query_params.get('trang_thai', '')
        if trang_thai:
            queryset = queryset.filter(trang_thai=trang_thai)
        
        serializer = SanPhamSerializer(queryset, many=True)
        
        return Response({
            'message': 'Danh sách sản phẩm',
            'user_role': request.user.role,
            'count': queryset.count(),
            'data': serializer.data
        })
    
    def post(self, request):
        """POST /sanpham/ - Tạo sản phẩm mới"""
        serializer = SanPhamSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            san_pham = serializer.save()
            return Response({
                'message': 'Tạo sản phẩm thành công',
                'user_role': request.user.role,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'message': 'Dữ liệu không hợp lệ',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class SanPhamDetailView(APIView):
    """API cho chi tiết sản phẩm"""
    permission_classes = [SanPhamPermission]
    
    def get(self, request, ma_sp):
        """GET /sanpham/{ma_sp}/ - Chi tiết sản phẩm"""
        try:
            san_pham = SanPham.objects.get(ma_sp=ma_sp)
            serializer = SanPhamSerializer(san_pham)
            
            return Response({
                'message': f'Chi tiết sản phẩm {ma_sp}',
                'user_role': request.user.role,
                'data': serializer.data
            })
        except SanPham.DoesNotExist:
            return Response({
                'message': 'Không tìm thấy sản phẩm'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, ma_sp):
        """PUT /sanpham/{ma_sp}/ - Cập nhật sản phẩm"""
        try:
            san_pham = SanPham.objects.get(ma_sp=ma_sp)
            serializer = SanPhamSerializer(san_pham, data=request.data, context={'request': request})
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': f'Cập nhật sản phẩm {ma_sp} thành công',
                    'user_role': request.user.role,
                    'data': serializer.data
                })
            
            return Response({
                'message': 'Dữ liệu không hợp lệ',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except SanPham.DoesNotExist:
            return Response({
                'message': 'Không tìm thấy sản phẩm'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, ma_sp):
        """PATCH /sanpham/{ma_sp}/ - Cập nhật một phần sản phẩm"""
        try:
            san_pham = SanPham.objects.get(ma_sp=ma_sp)
            serializer = SanPhamSerializer(san_pham, data=request.data, partial=True, context={'request': request})
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': f'Cập nhật một phần sản phẩm {ma_sp} thành công',
                    'user_role': request.user.role,
                    'data': serializer.data
                })
            
            return Response({
                'message': 'Dữ liệu không hợp lệ',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except SanPham.DoesNotExist:
            return Response({
                'message': 'Không tìm thấy sản phẩm'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, ma_sp):
        """DELETE /sanpham/{ma_sp}/ - Xóa sản phẩm"""
        try:
            san_pham = SanPham.objects.get(ma_sp=ma_sp)
            
            # Soft delete
            san_pham.is_active = False
            san_pham.trang_thai = 'ngung_ban'
            san_pham.save()
            
            return Response({
                'message': f'Xóa sản phẩm {ma_sp} thành công',
                'user_role': request.user.role
            }, status=status.HTTP_204_NO_CONTENT)
            
        except SanPham.DoesNotExist:
            return Response({
                'message': 'Không tìm thấy sản phẩm'
            }, status=status.HTTP_404_NOT_FOUND)