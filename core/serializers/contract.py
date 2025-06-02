from rest_framework import serializers
from core.models.contract import HOPDONG
from core.serializers.customer import KhachHangSerializer
from core.serializers.product import LoaiSanPhamSerializer

class HopDongSerializer(serializers.ModelSerializer):
    MA_KH_detail = KhachHangSerializer(source='MA_KH', read_only=True)
    MA_SP_detail = LoaiSanPhamSerializer(source='MA_SP', read_only=True)
    
    class Meta:
        model = HOPDONG
        fields = '__all__'