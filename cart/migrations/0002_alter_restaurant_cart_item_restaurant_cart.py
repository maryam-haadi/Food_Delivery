# Generated by Django 5.0.7 on 2024-07-18 08:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant_cart_item',
            name='restaurant_cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='cart.restaurant_cart'),
        ),
    ]
