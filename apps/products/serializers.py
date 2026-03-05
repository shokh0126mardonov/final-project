from rest_framework import serializers

from .models import Product
from apps.sellers.serializers import SellerProfileCreateSerializer

from rest_framework import serializers
from .models import Product


class ProductSerializers(serializers.ModelSerializer):

    seller = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Product
        fields = [
            "id",
            "seller",
            "title",
            "category",
            "description",
            "condition",
            "price",
            "price_type",
            "region",
            "district",
            "view_count",
            "favorite_count",
            "status",
            "created_at",
            "published_at",
            "expires_at",
        ]
