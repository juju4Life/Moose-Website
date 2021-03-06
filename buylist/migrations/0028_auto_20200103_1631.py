# Generated by Django 2.2.2 on 2020-01-03 21:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('buylist', '0027_auto_20191218_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='storecredit',
            name='customer_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='storecredit',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='storecredit',
            name='store_credit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
