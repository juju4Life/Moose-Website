# Generated by Django 2.1.4 on 2019-01-23 20:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0093_auto_20190123_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 23, 15, 10, 16, 395747), verbose_name='Order Placed'),
        ),
    ]