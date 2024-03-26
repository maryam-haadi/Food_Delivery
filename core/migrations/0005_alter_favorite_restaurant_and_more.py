# Generated by Django 5.0.3 on 2024-03-26 07:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_favorite_cofe_remove_cofefood_cofe_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favs', to='core.restaurant'),
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('user', 'restaurant')},
        ),
    ]
