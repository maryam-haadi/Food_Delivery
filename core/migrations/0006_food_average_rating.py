# Generated by Django 5.0.7 on 2024-08-17 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_food_image_alter_restaurant_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='average_rating',
            field=models.FloatField(blank=True, default=None),
        ),
    ]
