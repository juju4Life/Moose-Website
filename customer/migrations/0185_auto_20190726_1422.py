# Generated by Django 2.2.2 on 2019-07-26 18:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0184_auto_20190725_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 26, 14, 22, 30, 814915), verbose_name='Order Placed'),
        ),
    ]
