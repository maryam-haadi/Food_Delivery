# Generated by Django 5.0.3 on 2024-03-31 10:23

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
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
            ],
            options={
                'unique_together': {('category_name',)},
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('name', models.CharField(max_length=150)),
                ('desc', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('food_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food', to='core.foodcategory')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_foods', to='core.menu')),
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
                ('is_open', models.BooleanField(blank=True, default=False)),
                ('owner', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='account.owner')),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='restaurant',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='menu', to='core.restaurant'),
        ),
        migrations.CreateModel(
            name='FoodCategoryRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=255)),
                ('cat_desc', models.TextField(blank=True)),
                ('admin_approval', models.BooleanField(blank=True, default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('restaurant', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_request', to='core.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='DeleteRestaurantRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField(blank=True)),
                ('admin_approval', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delete_request', to='core.restaurant')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together={('restaurant',)},
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favs', to='core.restaurant')),
            ],
            options={
                'unique_together': {('user', 'restaurant')},
            },
        ),
    ]
