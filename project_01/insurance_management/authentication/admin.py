from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile
from core.models import Address

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_verified', 'is_active')
    list_filter = ('role', 'is_verified', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Thông tin bổ sung', {
            'fields': ('phone', 'role', 'is_verified', 'date_of_birth')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Thông tin bổ sung', {
            'fields': ('email', 'phone', 'role', 'first_name', 'last_name')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'identification_number', 'created_at')
    search_fields = ('user__username', 'identification_number')
    list_filter = ('created_at', 'is_active')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'ward', 'district', 'city', 'country')
    search_fields = ('street', 'district', 'city')
    list_filter = ('city', 'country')