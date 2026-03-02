from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SellerProfile (models.Model):
    user = models.OneToOneField(User,related_name="sellerprofile", on_delete=models.CASCADE,verbose_name="Do'kon egasi")
    shop_name = models.CharField(unique=True,verbose_name="Do'kon nomi")
    shop_description = models.TextField(blank=True,null=True,verbose_name="Do'kon tarifi")
    shop_logo = models.ImageField(upload_to="seller/%Y/%m/%d/",blank=True,null=True,verbose_name="Do'kon logosi")
    region = models.CharField(verbose_name="Viloyat")
    district = models.CharField(verbose_name="Tuman")
    address = models.CharField(blank=True,verbose_name="Manzili")
    rating = models.FloatField(default=0,verbose_name="O'rtacha reyting")
    total_sales = models.PositiveIntegerField(default=0,verbose_name="Sotuvlar soni")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  f"{self.id} {self.user.username}"
