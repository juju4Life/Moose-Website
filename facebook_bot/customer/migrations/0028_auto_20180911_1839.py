# Generated by Django 2.0 on 2018-09-11 22:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0027_auto_20180911_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 11, 18, 39, 37, 122130), verbose_name='Order Placed'),
        ),
        migrations.AlterField(
            model_name='releasedproducts',
            name='year',
            field=models.CharField(default='', max_length=255),
        ),
    ]
