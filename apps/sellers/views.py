from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import SellerProfileCreateSerializer
from .permissions import IsUserPermissions
from .models import SellerProfile

class SellerProfile(ModelViewSet):
    queryset = SellerProfile.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsUserPermissions]
    serializer_class = SellerProfileCreateSerializer

    def perform_create(self, serializer):
        serializer.save()
