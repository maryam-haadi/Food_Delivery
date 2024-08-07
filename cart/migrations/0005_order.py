# Generated by Django 5.0.7 on 2024-07-19 10:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_restaurant_cart_item_quantity'),
        ('core', '0002_alter_food_price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('paid', models.BooleanField(default=False)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cart.restaurant_cart')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='res_orders', to='core.restaurant')),
            ],
        ),
    ]
