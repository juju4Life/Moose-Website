# Generated by Django 2.2.2 on 2020-01-20 20:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0239_auto_20200115_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 20, 15, 49, 17, 450418), verbose_name='Order Placed'),
        ),
    ]
