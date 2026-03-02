from django.db import models


from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "customer", "Xaridor"
        SELLER = "seller", "Sotuvchi"

    chat_id = models.BigIntegerField(unique=True,null=True,blank=True)
    phone_number = models.CharField(max_length=20,blank=True,)
    role = models.CharField(max_length=20,choices=Role.choices,default=Role.CUSTOMER)
    avatar = models.ImageField(upload_to="avatars/%Y/%m/%d/",blank=True,null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
    def is_user(self):
        return self.role == self.Role.CUSTOMER
    
    def is_seller(self):
        return self.role == self.Role.SELLER