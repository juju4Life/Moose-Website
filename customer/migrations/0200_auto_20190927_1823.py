# Generated by Django 2.2.2 on 2019-09-27 22:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0199_auto_20190927_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 27, 18, 23, 36, 572729), verbose_name='Order Placed'),
        ),
    ]
