# Generated by Django 2.2.2 on 2019-09-13 17:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0196_auto_20190913_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 13, 13, 59, 35, 75586), verbose_name='Order Placed'),
        ),
    ]
