# Generated by Django 2.2.2 on 2019-12-18 22:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0221_auto_20191209_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 18, 17, 24, 10, 269548), verbose_name='Order Placed'),
        ),
    ]
