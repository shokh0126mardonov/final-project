from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Category
from .serializers import CategorySerializers
from apps.products.serializers import ProductSerializers
from apps.products.models import Product


class CategoryViewSets(ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CategorySerializers
    lookup_field = "slug"


class CategoryActiveProduct(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request, slug: str) -> Response:
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category).all()
        return Response(ProductSerializers(products, many=True).data)
