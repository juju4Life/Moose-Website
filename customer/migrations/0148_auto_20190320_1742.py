# Generated by Django 2.1.4 on 2019-03-20 21:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0147_auto_20190320_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 20, 17, 42, 7, 115480), verbose_name='Order Placed'),
        ),
    ]
