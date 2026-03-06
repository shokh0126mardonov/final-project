from django.contrib.auth import get_user_model
import redis


from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serailizers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status

from .serailizers import UserUpdateSerializer


User = get_user_model()

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        chat_id = request.query_params.get("chat_id")

        if not chat_id:
            return Response({"error": "chat_id required"}, status=400)

        user = User.objects.filter(chat_id=chat_id).first()

        if user:
            return Response({"status": True})

        return Response({"status": False})

    def post(self, request: Request) -> Response:

        serializers = UserSerializer(data=request.data)

        if serializers.is_valid(raise_exception=True):
            user = serializers.save()
            return Response({"status": True}, status=200)


class TelegramLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        r_code = request.data.get("r_code")

        if r_code is None or len(r_code) != 6 or not r_code.isdigit():
            return Response({"code": "error"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = r.get(f"login_code:{r_code}")

        if not user_id:
            return Response(
                {"error": "Kod xato yoki muddati o‘tgan"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(chat_id=user_id)
        except User.DoesNotExist:
            return Response("user not found", status=400)

        r.delete(f"login_user:{user_id}")
        r.delete(f"{f'login_code:{r_code}'}")

        token = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(token),
                "access": str(token.access_token),
            },
            status=200,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out"}, status=200)
        except Exception:
            return Response({"error": "Invalid token"}, status=400)


class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request: Request) -> Response:
        return Response(UserSerializer(request.user).data)

    def patch(self, request: Request) -> Response:
        user = request.user

        serializers = UserUpdateSerializer(data=request.data, partial=True)

        if serializers.is_valid(raise_exception=True):
            update_user = serializers.update(user, request.data)

            return Response(UserSerializer(update_user).data)
