# Generated by Django 2.1.4 on 2019-03-20 17:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0143_auto_20190311_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 20, 13, 6, 37, 273463), verbose_name='Order Placed'),
        ),
    ]
