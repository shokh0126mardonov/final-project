from rest_framework.permissions import BasePermission


class IsUserPermissions(BasePermission):
    message = "siz user emassiz"
    
    def has_permission(self, request, view):
        return request.user and request.user.is_user