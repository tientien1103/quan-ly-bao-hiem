from rest_framework import generics
from core.models.customer import KHACHHANG
from core.serializers.customer import KhachHangSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class KhachHangListCreateView(generics.ListCreateAPIView):
    queryset = KHACHHANG.objects.all()
    serializer_class = KhachHangSerializer

class KhachHangRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KHACHHANG.objects.all()
    serializer_class = KhachHangSerializer

@api_view(['POST'])
def create_khachhang(request):
    pass

@api_view(['GET'])
def get_khachhang(request, ma_kh):
    pass

@api_view(['GET'])
def list_khachhang(request):
    pass

@api_view(['PUT'])
def update_khachhang(request, ma_kh):
    pass

@api_view(['DELETE'])
def delete_khachhang(request, ma_kh):
    pass