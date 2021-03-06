# Generated by Django 2.1.4 on 2019-02-19 03:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20190218_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='total_quantity_sold',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='neworders',
            name='check_order_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
