from django.urls import path

from .views import RegisterAPIView,UserProfileView,TelegramLoginView

urlpatterns = [
    path("api/telegram-login/",TelegramLoginView.as_view()),
    path("user/register/",RegisterAPIView.as_view()),
    path("api/v1/users/me/",UserProfileView.as_view())

]
