# Generated by Django 5.0.7 on 2024-07-27 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_alter_payment_cvv2_alter_payment_daynamic_password_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='payment',
            unique_together={('order', 'origin_card_number')},
        ),
    ]
