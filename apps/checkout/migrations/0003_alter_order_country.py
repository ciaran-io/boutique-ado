# Generated by Django 4.2.3 on 2023-07-25 12:58

import django_countries.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_order_original_cart_order_stripe_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]