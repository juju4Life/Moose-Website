# Generated by Django 2.2.2 on 2019-11-09 17:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0206_auto_20191019_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 9, 12, 31, 5, 254589), verbose_name='Order Placed'),
        ),
    ]