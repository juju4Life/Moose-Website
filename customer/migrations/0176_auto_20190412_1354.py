# Generated by Django 2.1.4 on 2019-04-12 17:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0175_auto_20190412_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 12, 13, 54, 48, 838426), verbose_name='Order Placed'),
        ),
    ]
