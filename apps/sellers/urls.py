from django.urls import path

from .views import SellerProfile

urlpatterns = [
    path("api/v1/users/me/upgrade-to-seller/",SellerProfile.as_view({"post":"create"})),
    path("api/v1/sellers/<int:pk>/",SellerProfile.as_view({"get":"retrieve"})),

]
