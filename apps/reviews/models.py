from django.db import models
from django.contrib.auth import get_user_model

from apps.orders.models import Order


User = get_user_model()


class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name="review")

    reviewer = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="given_reviews"
    )

    seller = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="received_reviews"
    )

    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
