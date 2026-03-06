from django.urls import path

from .views import ProductViewSets, ProductUpdate, FavouriteViewSets

urlpatterns = [
    path(
        "api/v1/products/", ProductViewSets.as_view({"get": "list", "post": "create"})
    ),
    path(
        "api/v1/products/<int:pk>/",
        ProductViewSets.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "api/v1/products/<int:pk>/publish/", ProductUpdate.as_view({"post": "publish"})
    ),
    path(
        "api/v1/products/<int:pk>/archive/", ProductUpdate.as_view({"post": "archive"})
    ),
    path("api/v1/products/<int:pk>/sold/", ProductUpdate.as_view({"post": "sold"})),
    # Favourite
    path(
        "api/v1/favorites/",
        FavouriteViewSets.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "api/v1/favorites/<int:pk>/", FavouriteViewSets.as_view({"delete": "destroy"})
    ),
]
