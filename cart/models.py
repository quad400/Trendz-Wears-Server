from django.db import models
from django.contrib.auth import get_user_model

from shortuuidfield import ShortUUIDField
from product.models import Product

User = get_user_model()

class Cart(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.id
    