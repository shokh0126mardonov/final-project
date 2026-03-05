from django.db import models
from django.contrib.auth import get_user_model

from apps.categories.models import Category

User = get_user_model()

class Product(models.Model):

    class ConditionChoices(models.TextChoices):
        new = "yangi","yangi"
        ideal = "ideal","ideal"
        yaxshi = "yaxshi","yaxshi"
        qoniqarli = "qoniqarli","qoniqarli"

    class StatusChoices(models.TextChoices):
        moderatsiyada = "moderatsiyada","moderatsiyada"
        aktiv = "aktiv","aktiv"
        rad_etilgan = "rad etilgan","rad etilgan"
        sotilgan = "sotilgan","sotilgan"
        arxivlangan = "arxivlangan","arxivlangan"

    class Price_type(models.TextChoices):
        qatiy = "qatiy","qatiy"
        kelishiladi = "kelishiladi","kelishiladi"
        bepul = "bepul","bepul"
        ayirboshlash = "ayirboshlash","ayirboshlash"


    seller = models.ForeignKey(User, on_delete=models.CASCADE,related_name="products")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    title = models.CharField(max_length=200)
    description = models.TextField()
    condition = models.CharField(max_length=50,choices=ConditionChoices.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_type = models.CharField(choices=Price_type.choices,max_length=20)
    region = models.CharField()
    district = models.CharField()
    view_count = models.PositiveIntegerField(default=0)
    favorite_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50,choices=StatusChoices.choices,default=StatusChoices.moderatsiyada)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True)
    expires_at = models.DateTimeField()

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product/%Y/%m/%d/")
    order = models.PositiveIntegerField()
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Favorite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
