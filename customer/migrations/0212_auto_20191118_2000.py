# Generated by Django 2.2.2 on 2019-11-19 01:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0211_auto_20191118_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 18, 20, 0, 47, 925472), verbose_name='Order Placed'),
        ),
    ]
