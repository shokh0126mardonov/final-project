from django.db import models
from django.contrib.auth import get_user_model

from apps.products.models import Product
from apps.sellers.models import SellerProfile

User = get_user_model()


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "kutilyapti", "Kutilyapti"
        AGREED = "kelishilgan", "Kelishilgan"
        COMPLETED = "sotib_olingan", "Sotib olingan"
        CANCELLED = "bekor_qilingan", "Bekor qilingan"

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="orders"
    )

    buyer = models.ForeignKey(User, on_delete=models.PROTECT, related_name="purchases")

    seller = models.ForeignKey(
        SellerProfile, on_delete=models.PROTECT, related_name="sales"
    )

    final_price = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        db_index=True,
    )

    meeting_location = models.CharField(max_length=255, blank=True)

    meeting_time = models.DateTimeField(null=True, blank=True)

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
