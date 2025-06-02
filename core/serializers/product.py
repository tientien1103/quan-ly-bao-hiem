from rest_framework import serializers
from core.models.product import LOAI_SANPHAM, PHI_COI, PHI_QUANLY

class LoaiSanPhamSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOAI_SANPHAM
        fields = '__all__'

class PhiCoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = PHI_COI
        fields = '__all__'

class PhiQuanLySerializer(serializers.ModelSerializer):
    class Meta:
        model = PHI_QUANLY
        fields = '__all__'