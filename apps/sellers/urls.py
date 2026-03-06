from django.urls import path

from .views import SellerProfileUrl, SellerDataUrl

urlpatterns = [
    path(
        "api/v1/users/me/upgrade-to-seller/",
        SellerProfileUrl.as_view({"post": "create"}),
    ),
    path("api/v1/sellers/<int:pk>/", SellerProfileUrl.as_view({"get": "retrieve"})),
    path("api/v1/sellers/<int:pk>/products/", SellerDataUrl.as_view()),
]
