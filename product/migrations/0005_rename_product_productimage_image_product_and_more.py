# Generated by Django 4.2.1 on 2023-10-20 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_productimage_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productimage',
            old_name='product',
            new_name='image_product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_images',
        ),
        migrations.AddField(
            model_name='product',
            name='product_images',
            field=models.ManyToManyField(blank=True, to='product.productimage'),
        ),
    ]
