from django.urls import path

from .views import SellerProfile

urlpatterns = [
    path("api/v1/users/me/upgrade-to-seller/",SellerProfile.as_view())
]
