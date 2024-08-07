# Generated by Django 5.0.7 on 2024-07-27 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_payment_cvv2_payment_daynamic_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='cvv2',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='daynamic_password',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='payment',
            name='origin_card_number',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='payment',
            name='verification',
            field=models.CharField(max_length=5),
        ),
    ]
