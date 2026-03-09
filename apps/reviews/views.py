from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSets(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.select_related("order", "reviewer", "seller")

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = super().get_queryset()

        seller_id = self.request.query_params.get("seller_id")

        if seller_id:
            queryset = queryset.filter(seller_id=seller_id)

        return queryset
