# Generated by Django 2.1.4 on 2018-12-31 15:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0073_auto_20181229_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 31, 10, 10, 29, 449992), verbose_name='Order Placed'),
        ),
    ]
