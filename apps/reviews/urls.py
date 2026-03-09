from django.urls import path
from .views import ReviewViewSets


review_list = ReviewViewSets.as_view({"get": "list", "post": "create"})

review_detail = ReviewViewSets.as_view({"get": "retrieve"})


urlpatterns = [
    path(
        "api/v1/reviews/",
        ReviewViewSets.as_view({"get": "list", "post": "create"}, name="reviews-list"),
    ),
    path(
        "api/v1/reviews/<int:pk>/",
        ReviewViewSets.as_view({"get": "retrieve"}, name="reviews-detail"),
    ),
]
