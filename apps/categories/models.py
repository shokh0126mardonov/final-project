from django.db import models


class Category(models.Model):
    name = models.CharField()
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    icon = models.ImageField(upload_to="category/%Y/%m/%d/", blank=True, null=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    order_num = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
