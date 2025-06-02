from rest_framework import generics
from core.models.contract import HOPDONG
from core.serializers.contract import HopDongSerializer
from core.services.contract_service import tinh_phi_thang
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class HopDongListCreateView(generics.ListCreateAPIView):
    queryset = HOPDONG.objects.all()
    serializer_class = HopDongSerializer

class HopDongRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HOPDONG.objects.all()
    serializer_class = HopDongSerializer

class TinhPhiThangView(generics.RetrieveAPIView):
    queryset = HOPDONG.objects.all()
    serializer_class = HopDongSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        thang_nam = request.query_params.get('thang_nam')
        phi = tinh_phi_thang(instance, thang_nam)
        return Response({'tong_phi': phi})

@api_view(['POST'])
def create_hopdong(request):
    pass

@api_view(['GET'])
def get_hopdong(request, ma_hd):
    pass

@api_view(['GET'])
def list_hopdong(request):
    pass

@api_view(['PUT'])
def update_hopdong(request, ma_hd):
    pass

@api_view(['GET'])
def tinh_phi(request, ma_hd, thang_nam):
    pass