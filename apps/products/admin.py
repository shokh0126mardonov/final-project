from django.contrib import admin

from .models import Product,ProductImage,Favorite

admin.site.register([Product,ProductImage,Favorite])