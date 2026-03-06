from django.urls import path

from .views import CategoryViewSets, CategoryActiveProduct

urlpatterns = [
    path("api/v1/categories/", CategoryViewSets.as_view({"get": "list"})),
    path(
        "api/v1/categories/<str:slug>/", CategoryViewSets.as_view({"get": "retrieve"})
    ),
    path(
        "api/v1/categories/<str:slug>/products/", view=CategoryActiveProduct.as_view()
    ),
]
