# Generated by Django 2.1.4 on 2019-02-22 23:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0121_auto_20190221_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 22, 18, 2, 58, 201688), verbose_name='Order Placed'),
        ),
    ]
