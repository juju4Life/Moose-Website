# Generated by Django 2.2.2 on 2019-07-23 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0032_inventory_amazon'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='tcg_direct',
            field=models.BooleanField(default=False),
        ),
    ]