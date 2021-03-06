# Generated by Django 2.1.4 on 2019-04-01 15:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0152_auto_20190330_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemizedpreorder',
            name='custom_price',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 1, 11, 14, 41, 712432), verbose_name='Order Placed'),
        ),
    ]
