from rest_framework import generics
from core.models.product import LOAI_SANPHAM, PHI_COI, PHI_QUANLY
from core.serializers.product import LoaiSanPhamSerializer, PhiCoiSerializer, PhiQuanLySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class LoaiSanPhamListCreateView(generics.ListCreateAPIView):
    queryset = LOAI_SANPHAM.objects.all()
    serializer_class = LoaiSanPhamSerializer

class LoaiSanPhamRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LOAI_SANPHAM.objects.all()
    serializer_class = LoaiSanPhamSerializer

class PhiCoiListCreateView(generics.ListCreateAPIView):
    queryset = PHI_COI.objects.all()
    serializer_class = PhiCoiSerializer

class PhiQuanLyRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = PHI_QUANLY.objects.all()
    serializer_class = PhiQuanLySerializer
    lookup_field = 'MA_SP'

@api_view(['GET'])
def list_sanpham(request):
    pass

@api_view(['GET'])
def get_sanpham(request, ma_sp):
    pass

@api_view(['GET'])
def get_phi_coi(request, ma_sp, tuoi, menh_gia):
    pass

@api_view(['POST'])
def create_phi_coi(request):
    pass

@api_view(['GET'])
def get_phi_quanly(request, ma_sp):
    pass