from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SellerProfile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(unique=True,verbose_name="Do'kon nomi")
    shop_description = models.TextField(blank=True,null=True)
    shop_logo = models.ImageField(upload_to=None,blank=True,null=True)