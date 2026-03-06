from django.urls import path

from .views import OrderViewSets

urlpatterns = [path("api/v1/orders/", OrderViewSets.as_view({"get": "list"}))]
