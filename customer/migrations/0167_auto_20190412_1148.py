# Generated by Django 2.1.4 on 2019-04-12 15:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0166_auto_20190411_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 12, 11, 48, 35, 276980), verbose_name='Order Placed'),
        ),
    ]
