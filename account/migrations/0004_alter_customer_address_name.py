# Generated by Django 5.0.7 on 2024-07-22 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_customer_address_customer_address_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
