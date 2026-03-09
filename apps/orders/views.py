from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Order
from .serializers import OrderSerializer


class OrderViewSets(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def get_queryset(self):
        user = self.request.user
        role = self.request.query_params.get("role")

        queryset = Order.objects.select_related("product", "buyer", "seller")

        if role == "seller":
            return queryset.filter(seller__user=user)

        if role == "buyer":
            return queryset.filter(buyer=user)

        return queryset.filter(Q(buyer=user) | Q(seller__user=user))

    def perform_create(self, serializer):
        product = serializer.validated_data["product"]

        serializer.save(buyer=self.request.user, seller=product.seller)

    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        if obj.buyer != user and obj.seller.user != user:
            raise PermissionDenied("You do not have permission to access this order")

        return obj

    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()

        if order.seller.user != request.user:
            raise PermissionDenied("Only seller can update order status")

        return super().partial_update(request, *args, **kwargs)
