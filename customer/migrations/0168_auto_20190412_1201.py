# Generated by Django 2.1.4 on 2019-04-12 16:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0167_auto_20190412_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 12, 12, 1, 42, 633594), verbose_name='Order Placed'),
        ),
    ]