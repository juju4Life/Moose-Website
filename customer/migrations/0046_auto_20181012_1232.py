# Generated by Django 2.0 on 2018-10-12 16:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0045_auto_20181011_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='tournament_entry',
            field=models.CharField(choices=[('none', 'None'), ('fnm', 'FNM'), ('ygo', 'Yugioh Locals')], default='None', max_length=255),
        ),
        migrations.AddField(
            model_name='historicalcustomer',
            name='tournament_entry',
            field=models.CharField(choices=[('none', 'None'), ('fnm', 'FNM'), ('ygo', 'Yugioh Locals')], default='None', max_length=255),
        ),
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 12, 12, 32, 22, 683013), verbose_name='Order Placed'),
        ),
    ]
