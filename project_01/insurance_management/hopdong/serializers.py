from rest_framework import serializers
from .models import HopDong
from khachhang.serializers import KhachHangSerializer
from sanpham.serializers import SanPhamSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class HopDongSerializer(serializers.ModelSerializer):
    khach_hang_info = KhachHangSerializer(source='khach_hang', read_only=True)
    san_pham_info = SanPhamSerializer(source='san_pham', read_only=True)
    trang_thai_display = serializers.CharField(source='get_trang_thai_display', read_only=True)
    ky_han_dong_phi_display = serializers.CharField(source='get_ky_han_dong_phi_display', read_only=True)
    so_thang_hieu_luc = serializers.ReadOnlyField()
    is_hieu_luc = serializers.ReadOnlyField()
    
    class Meta:
        model = HopDong
        fields = '__all__'
        read_only_fields = ('ma_hd',)
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['nhan_vien_ban'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super().update(instance, validated_data)
    
    def validate(self, data):
        # Validation logic
        if data.get('ngay_hieu_luc') and data.get('ngay_ket_thuc'):
            if data['ngay_hieu_luc'] >= data['ngay_ket_thuc']:
                raise serializers.ValidationError("Ngày hiệu lực phải trước ngày kết thúc")
        
        # Kiểm tra tuổi khách hàng với sản phẩm
        khach_hang = data.get('khach_hang')
        san_pham = data.get('san_pham')
        
        if khach_hang and san_pham:
            tuoi_kh = khach_hang.tuoi
            if tuoi_kh < san_pham.tuoi_toi_thieu or tuoi_kh > san_pham.tuoi_toi_da:
                raise serializers.ValidationError(
                    f"Tuổi khách hàng ({tuoi_kh}) không phù hợp với sản phẩm (yêu cầu: {san_pham.tuoi_toi_thieu}-{san_pham.tuoi_toi_da} tuổi)"
                )
        
        # Kiểm tra số tiền bảo hiểm
        if san_pham and data.get('so_tien_bao_hiem'):
            so_tien = data['so_tien_bao_hiem']
            if so_tien < san_pham.so_tien_bao_hiem_toi_thieu or so_tien > san_pham.so_tien_bao_hiem_toi_da:
                raise serializers.ValidationError(
                    f"Số tiền bảo hiểm không hợp lệ (yêu cầu: {san_pham.so_tien_bao_hiem_toi_thieu:,.0f} - {san_pham.so_tien_bao_hiem_toi_da:,.0f} VND)"
                )
        
        return data

class TinhPhiHopDongSerializer(serializers.Serializer):
    """Serializer cho tính phí hợp đồng"""
    thang_nam = serializers.DateField()