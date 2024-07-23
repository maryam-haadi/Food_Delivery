# Generated by Django 5.0.7 on 2024-07-23 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_alter_order_paid_alter_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_address_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]