from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Chỉ cho phép owner chỉnh sửa, người khác chỉ đọc"""
    
    def has_object_permission(self, request, view, obj):
        # Quyền đọc cho tất cả authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Quyền ghi chỉ cho owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user

class IsAdminOrManager(permissions.BasePermission):
    """Chỉ admin và manager mới có quyền"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in ['admin', 'manager']
        )

class IsAdminOnly(permissions.BasePermission):
    """Chỉ admin mới có quyền"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role == 'admin'
        )

class IsAgentOrAbove(permissions.BasePermission):
    """Agent trở lên (Agent, Manager, Admin)"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in ['agent', 'manager', 'admin']
        )