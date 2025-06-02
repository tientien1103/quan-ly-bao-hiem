from rest_framework import serializers
from core.models.payment import PHI_THANHTOAN, LICHSU_THANHTOAN
from core.serializers.contract import HopDongSerializer

class PhiThanhToanSerializer(serializers.ModelSerializer):
    MA_HD_detail = HopDongSerializer(source='MA_HD', read_only=True)
    
    class Meta:
        model = PHI_THANHTOAN
        fields = '__all__'

class LichSuThanhToanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LICHSU_THANHTOAN
        fields = '__all__'