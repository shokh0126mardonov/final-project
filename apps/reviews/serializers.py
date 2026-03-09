from rest_framework import serializers
from .models import Review
from apps.orders.models import Order


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "order",
            "reviewer",
            "seller",
            "rating",
            "comment",
            "created_at",
        ]

        read_only_fields = [
            "reviewer",
            "seller",
            "created_at",
        ]

    def validate(self, attrs):
        request = self.context["request"]
        order = attrs["order"]

        # faqat buyer review yozishi mumkin
        if order.buyer != request.user:
            raise serializers.ValidationError("Only buyer can leave review")

        # order completed bo'lishi kerak
        if order.status != "sotib_olingan":
            raise serializers.ValidationError(
                "Review allowed only after completed order"
            )

        return attrs

    def create(self, validated_data):
        order = validated_data["order"]
        request = self.context["request"]

        validated_data["reviewer"] = request.user
        validated_data["seller"] = order.seller.user

        return super().create(validated_data)
