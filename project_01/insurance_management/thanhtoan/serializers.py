from rest_framework import serializers
from .models import ThanhToan, CongNo

class ThanhToanSerializer(serializers.ModelSerializer):
    hop_dong_info = serializers.StringRelatedField(source='hop_dong', read_only=True)
    phi_thanh_toan_info = serializers.StringRelatedField(source='phi_thanh_toan', read_only=True)
    trang_thai_display = serializers.CharField(source='get_trang_thai_display', read_only=True)
    phuong_thuc_display = serializers.CharField(source='get_phuong_thuc_thanh_toan_display', read_only=True)
    
    class Meta:
        model = ThanhToan
        fields = '__all__'
        read_only_fields = ('ma_thanh_toan',)
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['nhan_vien_xu_ly'] = self.context['request'].user
        return super().create(validated_data)

class CongNoSerializer(serializers.ModelSerializer):
    hop_dong_info = serializers.StringRelatedField(source='hop_dong', read_only=True)
    so_ngay_tre_han = serializers.ReadOnlyField()
    tong_cong_no = serializers.ReadOnlyField()
    
    class Meta:
        model = CongNo
        fields = '__all__'
        read_only_fields = ('ma_cong_no',)
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)