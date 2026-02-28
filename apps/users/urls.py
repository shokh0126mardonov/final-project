from django.urls import path

from .views import RegisterAPIView

urlpatterns = [
    path("user/register/",RegisterAPIView.as_view())
]
