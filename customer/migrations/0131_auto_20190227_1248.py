# Generated by Django 2.1.4 on 2019-02-27 17:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0130_auto_20190227_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 27, 12, 48, 1, 322251), verbose_name='Order Placed'),
        ),
    ]
