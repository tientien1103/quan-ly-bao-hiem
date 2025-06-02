from rest_framework import generics
from core.models.payment import PHI_THANHTOAN, LICHSU_THANHTOAN
from core.serializers.payment import PhiThanhToanSerializer, LichSuThanhToanSerializer
from core.services.payment_service import get_thang_no
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class PhiThanhToanListCreateView(generics.ListCreateAPIView):
    queryset = PHI_THANHTOAN.objects.all()
    serializer_class = PhiThanhToanSerializer

class LichSuThanhToanListCreateView(generics.ListCreateAPIView):
    queryset = LICHSU_THANHTOAN.objects.all()
    serializer_class = LichSuThanhToanSerializer

class ThangNoListView(generics.RetrieveAPIView):
    queryset = PHI_THANHTOAN.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        ma_hd = kwargs.get('ma_hd')
        thang_no = get_thang_no(ma_hd)
        return Response({'thang_no': thang_no})

@api_view(['GET'])
def get_danh_sach_phi(request, ma_hd):
    pass

@api_view(['POST'])
def tao_phi_thang(request):
    pass

@api_view(['GET'])
def list_lich_su_thanhtoan(request, ma_hd):
    pass

@api_view(['POST'])
def create_thanhtoan(request):
    pass

@api_view(['GET'])
def get_thanh_toan(request, ma_hd):
    pass