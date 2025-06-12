from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import UserProfile
from .serializers import (
    UserRegistrationSerializer, 
    UserSerializer, 
    UserProfileSerializer
)
from .permissions import IsOwnerOrReadOnly, IsAdminOrManager

User = get_user_model()

class RegisterView(APIView):
    """API đăng ký tài khoản"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Tạo JWT token
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Đăng ký thành công'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    """API đăng xuất"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Đăng xuất thành công'})
        except Exception as e:
            return Response({'error': 'Token không hợp lệ'}, 
                          status=status.HTTP_400_BAD_REQUEST)

class CurrentUserView(APIView):
    """API lấy thông tin user hiện tại"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """Cập nhật thông tin user hiện tại"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet quản lý Users với phân quyền"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """Phân quyền theo action"""
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['list']:
            permission_classes = [permissions.IsAuthenticated, IsAdminOrManager]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter queryset theo quyền"""
        user = self.request.user
        if user.role == 'admin':
            return User.objects.all()
        elif user.role == 'manager':
            # Manager có thể xem admin và những user cấp thấp hơn
            return User.objects.exclude(role='admin')
        else:
            # Agent và Customer chỉ xem được chính mình
            return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Lấy thông tin user hiện tại"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrManager])
    def verify(self, request, pk=None):
        """Xác thực user (chỉ admin/manager)"""
        user = self.get_object()
        user.is_verified = True
        user.save()
        return Response({'message': f'Đã xác thực user {user.username}'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet quản lý User Profiles"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """Filter theo quyền"""
        if self.request.user.role in ['admin', 'manager']:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Tự động gán user hiện tại"""
        serializer.save(user=self.request.user)