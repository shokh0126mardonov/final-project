from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import SellerProfileCreateSerializer
from .models import SellerProfile
from apps.products.serializers import ProductSerializers


class SellerProfileUrl(ModelViewSet):
    queryset = SellerProfile.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = SellerProfileCreateSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()


class SellerDataUrl(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request, pk: int) -> Response:
        seller = get_object_or_404(SellerProfile, pk=pk)
        products = seller.user.products.all()

        data = []
        for product in products:
            if product.status == "aktiv":
                data.append(product)

        return Response(ProductSerializers(data, many=True).data)
