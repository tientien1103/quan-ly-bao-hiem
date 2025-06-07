from rest_framework import permissions

class RoleBasedPermission(permissions.BasePermission):
    """Base permission class cho phân quyền theo vai trò"""
    
    permission_map = {}
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        user_role = request.user.role
        action = self._get_action_from_method(request.method)
        
        allowed_roles = self.permission_map.get(action, [])
        
        return user_role in allowed_roles
    
    def _get_action_from_method(self, method):
        method_action_map = {
            'GET': 'list',
            'POST': 'create', 
            'PUT': 'update',
            'PATCH': 'partial_update',
            'DELETE': 'destroy'
        }
        return method_action_map.get(method, 'list')

class KhachHangPermission(RoleBasedPermission):
    permission_map = {
        'list': ['admin', 'manager', 'agent'],
        'create': ['admin', 'manager', 'agent'],
        'update': ['admin', 'manager', 'agent'],
        'partial_update': ['admin', 'manager', 'agent'],
        'destroy': ['admin', 'manager'],
    }

class KhachHangDetailPermission(RoleBasedPermission):
    permission_map = {
        'list': ['admin', 'manager', 'agent', 'customer'],
        'update': ['admin', 'manager', 'agent'],
        'partial_update': ['admin', 'manager', 'agent'],
        'destroy': ['admin', 'manager'],
    }

class SanPhamPermission(RoleBasedPermission):
    permission_map = {
        'list': ['admin', 'manager', 'agent', 'customer'],
        'create': ['admin', 'manager'],
        'update': ['admin', 'manager'],
        'partial_update': ['admin', 'manager'],
        'destroy': ['admin'],
    }

class HopDongPermission(RoleBasedPermission):
    permission_map = {
        'list': ['admin', 'manager', 'agent', 'customer'],
        'create': ['admin', 'manager', 'agent'],
        'update': ['admin', 'manager'],
        'partial_update': ['admin', 'manager'],
        'destroy': ['admin'],
    }

class PhiPermission(RoleBasedPermission):
    permission_map = {
        'list': ['admin', 'manager', 'agent', 'customer'],
        'create': ['admin', 'manager', 'agent'],
    }

class ThanhToanPermission(RoleBasedPermission):
    permission_map = {
        'list': ['admin', 'manager', 'agent'],
        'create': ['admin', 'manager', 'agent'],
    }

class ThanhToanDetailPermission(RoleBasedPermission):
    permission_map = {
        'list': ['admin', 'manager', 'agent', 'customer'],
    }