# Generated by Django 5.0.7 on 2024-08-18 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0021_alter_chancespining_absurd_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chancespining',
            name='absurd',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chancespining',
            name='amount_discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='chancespining',
            name='percentage_discount',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]