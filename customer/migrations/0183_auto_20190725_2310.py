# Generated by Django 2.2.2 on 2019-07-26 03:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0182_auto_20190725_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 25, 23, 10, 49, 740533), verbose_name='Order Placed'),
        ),
    ]
