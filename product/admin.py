from django.contrib import admin

from .models import Product, ProductColor, ProductImage, ProductSizes
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductColor)
admin.site.register(ProductImage)
admin.site.register(ProductSizes)