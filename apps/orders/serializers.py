from rest_framework import serializers

from .models import Order

from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    buyer = serializers.PrimaryKeyRelatedField(read_only=True)
    seller = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "product",
            "buyer",
            "seller",
            "final_price",
            "status",
            "meeting_location",
            "meeting_time",
            "notes",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "buyer",
            "seller",
            "status",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        request = self.context["request"]
        product = validated_data["product"]

        validated_data["buyer"] = request.user
        validated_data["seller"] = product.seller

        return super().create(validated_data)
