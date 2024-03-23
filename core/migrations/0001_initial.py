# Generated by Django 5.0.3 on 2024-03-23 18:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200)),
                ('category_desc', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200)),
                ('category_desc', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Cofe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('delivery_time', models.CharField(max_length=80)),
                ('min_cart_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('delivery_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('name', models.CharField(max_length=200)),
                ('phone_number', models.CharField(blank=True, max_length=50)),
                ('open_time', models.TimeField()),
                ('close_time', models.TimeField()),
                ('is_favorite', models.BooleanField(blank=True, default=False)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='account.address')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cofe', to='account.owner')),
            ],
        ),
        migrations.CreateModel(
            name='CofeFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('name', models.CharField(max_length=150)),
                ('desc', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('cofe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coffoods', to='core.cofe')),
                ('food_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foods', to='core.foodcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('delivery_time', models.CharField(max_length=80)),
                ('min_cart_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('delivery_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('name', models.CharField(max_length=200)),
                ('phone_number', models.CharField(blank=True, max_length=50)),
                ('open_time', models.TimeField()),
                ('close_time', models.TimeField()),
                ('is_favorite', models.BooleanField(blank=True, default=False)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='account.address')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='account.owner')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurants', to='core.restaurantcategory')),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('name', models.CharField(max_length=150)),
                ('desc', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('food_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food', to='core.foodcategory')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resfoods', to='core.restaurant')),
            ],
        ),
    ]
