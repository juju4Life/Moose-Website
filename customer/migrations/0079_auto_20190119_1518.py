# Generated by Django 2.1.4 on 2019-01-19 20:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0078_auto_20190119_0310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 19, 15, 17, 47, 961847), verbose_name='Order Placed'),
        ),
    ]