# Generated by Django 2.0 on 2018-11-15 01:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0057_auto_20181114_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 14, 20, 37, 48, 211133), verbose_name='Order Placed'),
        ),
    ]
