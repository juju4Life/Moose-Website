# Generated by Django 2.1.4 on 2019-03-03 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0026_inventory_custom_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupname',
            name='added',
            field=models.BooleanField(default=False),
        ),
    ]