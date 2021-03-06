# Generated by Django 3.0.5 on 2020-07-06 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0054_auto_20200706_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='completedorder',
            name='company',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='company',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='pendingpaymentorder',
            name='company',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='pullingorder',
            name='company',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='readytoshiporder',
            name='company',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
