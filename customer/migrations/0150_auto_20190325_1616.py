# Generated by Django 2.1.4 on 2019-03-25 20:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0149_auto_20190323_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 25, 16, 15, 55, 214289), verbose_name='Order Placed'),
        ),
    ]