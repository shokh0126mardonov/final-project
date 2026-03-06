from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterAPIView, UserProfileView, TelegramLoginView, LogoutView

urlpatterns = [
    # Auht url
    path("user/register/", RegisterAPIView.as_view()),
    path("api/telegram-login/", TelegramLoginView.as_view()),
    path("api/v1/auth/refresh/", TokenRefreshView.as_view()),
    path("api/v1/auth/logout/", LogoutView.as_view()),
    # user url
    path("api/v1/users/me/", UserProfileView.as_view()),
]
