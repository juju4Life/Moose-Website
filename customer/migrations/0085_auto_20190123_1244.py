# Generated by Django 2.1.4 on 2019-01-23 17:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0084_auto_20190123_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 23, 12, 44, 44, 411160), verbose_name='Order Placed'),
        ),
    ]
