from django.contrib.auth import get_user_model

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serailizers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
import redis


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
            return Response({"status":True},status=200)

class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def get(self, request:Request)->Response:
        print("USER:", request.user)
        print("ID:", request.user.id)
        print("CHAT_ID:", request.user.chat_id)
        return Response(UserSerializer(request.user).data)
       
r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    decode_responses=True
)
import redis
import re

from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

r = redis.Redis(
    host="127.0.0.1",
    port=6379,
    decode_responses=True
)


class TelegramLoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request:Request)->Response:
        r_code = request.data.get("r_code")

        if r_code is None or len(r_code) != 6 or not r_code.isdigit():
            return Response({"code":"error"},status=status.HTTP_400_BAD_REQUEST)
        
        user_id = r.get(f"login_code:{r_code}")

        if not user_id:
            return Response(
                {"error": "Kod xato yoki muddati o‘tgan"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(chat_id = user_id)
        except User.DoesNotExist:
            return Response("user not found",status=400)
        
        r.delete(f"login_user:{user_id}")
        r.delete(f"{f"login_code:{r_code}"}")

        token = RefreshToken.for_user(user)

        return Response({
                "refresh": str(token),
                "access": str(token.access_token),
            },status=200)

