# Generated by Django 2.1.4 on 2019-04-06 15:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0158_auto_20190406_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 6, 11, 40, 10, 835775), verbose_name='Order Placed'),
        ),
    ]
