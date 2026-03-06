from rest_framework.permissions import BasePermission


class IsSellerPermissions(BasePermission):
    message = "siz sotuvchi emassiz"

    def has_permission(self, request, view):
        return request.user and request.user.is_seller


class IsOwnerSellerPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user
