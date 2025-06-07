from rest_framework import serializers
from .models import SanPham

class SanPhamSerializer(serializers.ModelSerializer):
    loai_san_pham_display = serializers.CharField(source='get_loai_san_pham_display', read_only=True)
    trang_thai_display = serializers.CharField(source='get_trang_thai_display', read_only=True)
    
    class Meta:
        model = SanPham
        fields = '__all__'
        read_only_fields = ('ma_sp',)
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super().update(instance, validated_data)
    
    def validate(self, data):
        # Validation logic
        if data.get('phi_bao_hiem_toi_thieu', 0) > data.get('phi_bao_hiem_toi_da', 0):
            raise serializers.ValidationError("Phí bảo hiểm tối thiểu không được lớn hơn tối đa")
        
        if data.get('so_tien_bao_hiem_toi_thieu', 0) > data.get('so_tien_bao_hiem_toi_da', 0):
            raise serializers.ValidationError("Số tiền bảo hiểm tối thiểu không được lớn hơn tối đa")
        
        if data.get('tuoi_toi_thieu', 0) > data.get('tuoi_toi_da', 0):
            raise serializers.ValidationError("Tuổi tối thiểu không được lớn hơn tối đa")
        
        if data.get('thoi_han_toi_thieu', 0) > data.get('thoi_han_toi_da', 0):
            raise serializers.ValidationError("Thời hạn tối thiểu không được lớn hơn tối đa")
        
        return data

class SanPhamTinhPhiSerializer(serializers.Serializer):
    """Serializer cho tính phí sản phẩm"""
    tuoi = serializers.IntegerField(min_value=0, max_value=120)
    so_tien_bao_hiem = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=0)