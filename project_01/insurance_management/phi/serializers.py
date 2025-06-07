from rest_framework import serializers
from .models import BangPhiCoi, PhiQuanLy, PhiThanhToan

class BangPhiCoiSerializer(serializers.ModelSerializer):
    san_pham_info = serializers.StringRelatedField(source='san_pham', read_only=True)
    
    class Meta:
        model = BangPhiCoi
        fields = '__all__'
        read_only_fields = ('ma_phi_coi',)
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class PhiQuanLySerializer(serializers.ModelSerializer):
    san_pham_info = serializers.StringRelatedField(source='san_pham', read_only=True)
    
    class Meta:
        model = PhiQuanLy
        fields = '__all__'
        read_only_fields = ('ma_phi_ql',)
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class PhiThanhToanSerializer(serializers.ModelSerializer):
    hop_dong_info = serializers.StringRelatedField(source='hop_dong', read_only=True)
    qua_han = serializers.ReadOnlyField()
    
    class Meta:
        model = PhiThanhToan
        fields = '__all__'
        read_only_fields = ('ma_phi_tt', 'tong_phi')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class TinhPhiCoiSerializer(serializers.Serializer):
    """Serializer cho tính phí coi"""
    ma_sp = serializers.CharField()
    tuoi = serializers.IntegerField(min_value=0, max_value=120)
    menh_gia = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=0)