# Generated by Django 2.2.2 on 2019-07-25 00:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0179_auto_20190723_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 24, 20, 38, 19, 897431), verbose_name='Order Placed'),
        ),
    ]