from rest_framework import serializers

from .models import (Product, ProductColor, ProductSizes, ProductImage)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image",)

    def validate_image(self, attr):
        if attr is None:
            raise serializers.ValidationError({"invalid_detail": "This cant be null"}, code=400)


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSizes
        fields = ("id", "name")


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ("id", "name")


class ProductSerializer(serializers.ModelSerializer):
    product_images = serializers.H(many=True, required=False, read_only=True)
    product_colors = ProductColorSerializer(many=True, required=False, read_only=True)
    product_sizes = ProductSizeSerializer(many=True, required=False, read_only=True)
    timestamp = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ("id", "name", "desc", "category", "type", "price",
                   "product_sizes","product_images", "product_colors", "timestamp",)

    def get_timestamp(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d')
