# Generated by Django 2.1.4 on 2019-04-06 16:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0159_auto_20190406_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='employee_initial',
            field=models.CharField(default='', max_length=5),
        ),
        migrations.AddField(
            model_name='historicalcustomer',
            name='employee_initial',
            field=models.CharField(default='', max_length=5),
        ),
        migrations.AddField(
            model_name='historicalpreordersready',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='historicalpreordersready',
            name='employee_initials',
            field=models.CharField(default='', max_length=5),
        ),
        migrations.AddField(
            model_name='historicalpreordersready',
            name='preorder_type',
            field=models.CharField(choices=[('sealed_product', 'Sealed Product'), ('single', 'Single'), ('other', 'Other')], default='Sealed Product', max_length=255),
        ),
        migrations.AddField(
            model_name='preordersready',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='preordersready',
            name='employee_initials',
            field=models.CharField(default='', max_length=5),
        ),
        migrations.AddField(
            model_name='preordersready',
            name='preorder_type',
            field=models.CharField(choices=[('sealed_product', 'Sealed Product'), ('single', 'Single'), ('other', 'Other')], default='Sealed Product', max_length=255),
        ),
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 6, 12, 2, 29, 580065), verbose_name='Order Placed'),
        ),
    ]