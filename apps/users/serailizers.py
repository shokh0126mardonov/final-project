from django.core.files.base import ContentFile
from django.db import transaction

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
import redis


from .services import get_image_by_id

User = get_user_model()


class UserSerializer(serializers.Serializer):
    chat_id = serializers.IntegerField()
    username = serializers.CharField(required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    avatar = serializers.CharField()

    @transaction.atomic
    def create(self, validated_data):
        file_id = validated_data.pop("avatar")
        chat_id = validated_data["chat_id"]

        user, created = User.objects.get_or_create(
            chat_id=chat_id,
            defaults={
                "username": validated_data.get("username") or str(chat_id),
                "first_name": validated_data["first_name"],
                "last_name": validated_data["last_name"],
                "phone_number": validated_data["phone_number"],
            },
        )

        if created:
            user.set_unusable_password()
            user.save()

        if file_id:
            image_bytes = get_image_by_id(file_id)
            user.avatar.save(f"{chat_id}.jpg", ContentFile(image_bytes), save=True)

        return user

    def validate_telegram_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("Invalid telegram_id")
        return value


class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    avatar = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save(update_fields=list(validated_data.keys()))
        return instance
