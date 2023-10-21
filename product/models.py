from django.db import models
from shortuuidfield import ShortUUIDField


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('jacket', 'Jacket'),
        ('tops', 'Tops'),
        ('jean', 'Jean'),
        ('gown', 'Gown'),
        ('jogger', 'Jogger'),
    ]

    TYPE_CHOICES = [
        ('women', 'Women'),
        ('men', 'Men'),
    ]

    id = ShortUUIDField(primary_key=True, editable=False, unique=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="all")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="all")
    name = models.CharField(max_length=150, unique=True)
    desc = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class ProductImage(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, unique=True)
    image_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    def __str__(self):
        return self.image_product.name
    

class ProductSizes(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, unique=True)
    size_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_sizes")
    name = models.CharField(max_length=4)

    def __str__(self) -> str:
        return self.name


class ProductColor(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, unique=True)
    color_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_colors")
    name = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name
