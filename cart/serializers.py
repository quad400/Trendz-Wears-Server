from rest_framework import serializers,status
from rest_framework.response import Response

from .models import Cart
from product.models import Product
from product.serializers import ProductImageSerializer

class CartProduct(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, required=False)
    class Meta:
        model = Product
        fields = ("name", "price", "product_images",)

class CartSerializer(serializers.ModelSerializer):
    cart_product = CartProduct(read_only=True)

    class Meta:
        model = Cart
        fields = ("id", "cart_product", "cartcolor", "cartsize", "ordered")
