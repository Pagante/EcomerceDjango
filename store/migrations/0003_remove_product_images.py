# Generated by Django 3.2.7 on 2021-09-02 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_productimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
    ]
