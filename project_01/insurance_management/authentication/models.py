from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import BaseModel, Address

class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Quản trị viên'
    MANAGER = 'manager', 'Quản lý'
    AGENT = 'agent', 'Đại lý'
    CUSTOMER = 'customer', 'Khách hàng'

class CustomUser(AbstractUser):
    """Mở rộng User model với phân quyền"""
    phone = models.CharField(max_length=20, unique=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER
    )
    is_verified = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
    
    def has_role(self, role):
        """Kiểm tra quyền của user"""
        return self.role == role
    
    def is_admin_or_manager(self):
        """Kiểm tra có phải admin hoặc manager"""
        return self.role in [UserRole.ADMIN, UserRole.MANAGER]

class UserProfile(BaseModel):
    """Profile mở rộng cho User"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    identification_number = models.CharField(max_length=50, unique=True, blank=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"
    
    class Meta:
        verbose_name = 'Hồ sơ người dùng'
        verbose_name_plural = 'Hồ sơ người dùng'