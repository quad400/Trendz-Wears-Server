import admin_thumbnails
from django.contrib import admin

from .models import Product, ProductColor, ProductImage, ProductSizes
# Register your models here.

@admin_thumbnails.thumbnail("image")
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ("id",)

class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1
    readonly_fields = ("id",)

class ProductSizeInline(admin.TabularInline):
    model = ProductSizes
    extra = 1
    readonly_fields = ("id",)

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "category"]
    inlines = [ProductImageInline, ProductSizeInline, ProductColorInline]

admin.site.register(Product, ProductAdmin)