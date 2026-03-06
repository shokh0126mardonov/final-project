from apps.users.serailizers import UserSerializer
from rest_framework import serializers

from .models import SellerProfile


class SellerProfileCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = SellerProfile
        fields = [
            "user",
            "shop_name",
            "shop_description",
            "shop_logo",
            "region",
            "district",
            "address",
        ]

    def create(self, validated_data):
        user = self.context["request"].user

        if hasattr(user, "sellerprofile"):
            raise serializers.ValidationError("Seller profile mavjud")

        seller_profile = SellerProfile.objects.create(user=user, **validated_data)

        user.role = "seller"
        user.save(update_fields=["role"])

        return seller_profile
