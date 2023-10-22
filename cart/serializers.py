from rest_framework import serializers

from .models import Cart
from product.models import Product

class CartProduct(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "price")

class CartSerializer(serializers.ModelSerializer):

    cart_product = CartProduct()
    size = serializers.CharField(reqired=False, max_length=6),
    color = serializers.CharField(required=False, max_length=15)

    class Meta:
        model = Cart
        fields = ("id", "cart_product", "ordered", "color",)
