# Generated by Django 2.0 on 2018-08-15 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0041_orders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='product_value',
        ),
    ]
