# Generated by Django 2.1.4 on 2019-04-12 00:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0161_auto_20190411_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 11, 20, 49, 11, 661359), verbose_name='Order Placed'),
        ),
    ]