from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Product, Favorite
from .serializers import ProductSerializers, FavoriteSerializers
from .permissions import IsSellerPermissions, IsOwnerSellerPermissions


class ProductViewSets(ModelViewSet):
    queryset = Product.objects.filter(status="aktiv").all()
    serializer_class = ProductSerializers

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        product.view_count += 1
        product.save()
        serializers = self.get_serializer(product)
        return Response(serializers.data)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsSellerPermissions]

        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsOwnerSellerPermissions]

        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]


class ProductUpdate(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = [IsAuthenticated]

    def publish(self, request, pk):
        product = self.get_object()

        if product.seller != request.user:
            return Response({"status": "permission denide"}, status=403)

        product.status = "aktiv"
        product.save(update_fields=["status"])

        return Response({"status": "publish"})

    def archive(self, request, pk):
        product = self.get_object()

        if product.seller != request.user:
            return Response({"status": "permission denide"}, status=403)

        product.status = "arxivlangan"
        product.save(update_fields=["status"])

        return Response({"status": "archive"})

    def sold(self, request, pk):
        product = self.get_object()

        if product.seller != request.user:
            return Response({"status": "permission denide"}, status=403)

        product.status = "sotilgan"
        product.save(update_fields=["status"])

        return Response({"status": "sold"})


class FavouriteViewSets(ModelViewSet):
    serializer_class = FavoriteSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
