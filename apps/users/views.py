import requests

from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serailizers import UserSerializer
from .services import get_image_by_id

User = get_user_model()


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request:Request)->Response:
        chat_id = request.query_params.get("chat_id")

        if not chat_id:
            return Response({"error": "chat_id required"}, status=400)

        user = User.objects.filter(chat_id=chat_id).first()

        if user:
            return Response({"status": True})

        return Response({"status": False})

    def post(self, request:Request)->Response:

        serializers = UserSerializer(data = request.data)

        if serializers.is_valid(raise_exception=True):
            user = serializers.save()
            return Response({"status":True})
