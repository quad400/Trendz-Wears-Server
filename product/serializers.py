from rest_framework import serializers

from .models import (Product, ProductColor, ProductSizes, ProductImage)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image",)

    # def create(self, validated_data):
    #     product_images = validated_data.pop("product_images")
    #     if Product.objects.filter(name=product_images.name).exists():
    #         raise serializers.ValidationError("Product image already exist")
    #     created_image = ProductImage.objects.create(product_images=product_images, **validated_data)
    #     return created_image


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSizes
        fields = ("id", "name")


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ("id", "name")


class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    product_colors = ProductColorSerializer(many=True)
    product_sizes = ProductSizeSerializer(many=True)

    class Meta:
        model = Product
        fields = ("id", "name", "desc", "category", "type", "price",
                   "product_sizes","product_images", "product_colors", "timestamp",)
