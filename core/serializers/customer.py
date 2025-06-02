from rest_framework import serializers
from core.models.customer import KHACHHANG

class KhachHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = KHACHHANG
        fields = '__all__'