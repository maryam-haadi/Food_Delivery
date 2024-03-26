# Generated by Django 5.0.3 on 2024-03-25 10:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('category', models.CharField(choices=[('iranian', 'iranian'), ('fastfood', 'fastfood'), ('kebab', 'kebab'), ('piza', 'piza'), ('burger', 'burger'), ('sandwich', 'sandwich'), ('fried', 'fried'), ('pasta', 'pasta'), ('salad', 'salad'), ('marine', 'marine'), ('International', 'International'), ('Gilani', 'Gilani')], max_length=255)),
                ('delivery_time', models.CharField(max_length=80)),
                ('min_cart_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('delivery_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('name', models.CharField(max_length=200)),
                ('phone_number', models.CharField(blank=True, max_length=50)),
                ('open_time', models.TimeField()),
                ('close_time', models.TimeField()),
                ('address_name', models.CharField(default='', max_length=200)),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='account.owner')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favs', to='core.restaurant')),
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
