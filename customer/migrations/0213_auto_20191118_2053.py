# Generated by Django 2.2.2 on 2019-11-19 01:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0212_auto_20191118_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 18, 20, 53, 24, 150828), verbose_name='Order Placed'),
        ),
    ]
