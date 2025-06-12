from rest_framework import serializers
from .models import KhachHang
from core.models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

class KhachHangSerializer(serializers.ModelSerializer):
    dia_chi = AddressSerializer(read_only=True)
    dia_chi_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(),
        source='dia_chi',
        write_only=True,
        required=False
    )
    tuoi = serializers.ReadOnlyField()
    
    class Meta:
        model = KhachHang
        fields = '__all__'
        read_only_fields = ('ma_kh', 'ngay_dang_ky', 'tuoi')
    
    def create(self, validated_data):
        # Tự động gán user hiện tại là người tạo
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Tự động gán user hiện tại là người cập nhật
        validated_data['updated_by'] = self.context['request'].user
        return super().update(instance, validated_data)

class KhachHangCreateSerializer(serializers.ModelSerializer):
    """Serializer riêng cho tạo khách hàng với địa chỉ"""
    dia_chi = AddressSerializer(required=False)
    
    class Meta:
        model = KhachHang
        exclude = ('ma_kh', 'ngay_dang_ky')
    
    def create(self, validated_data):
        dia_chi_data = validated_data.pop('dia_chi', None)
        validated_data['created_by'] = self.context['request'].user
        
        # Tạo địa chỉ nếu có
        if dia_chi_data:
            dia_chi_data['created_by'] = self.context['request'].user
            dia_chi = Address.objects.create(**dia_chi_data)
            validated_data['dia_chi'] = dia_chi
        
        return KhachHang.objects.create(**validated_data)