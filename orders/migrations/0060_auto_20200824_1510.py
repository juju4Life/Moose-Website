# Generated by Django 3.0.5 on 2020-08-24 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0059_auto_20200717_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='completedorder',
            name='order_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pendingpaymentorder',
            name='order_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pullingorder',
            name='order_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='readytoshiporder',
            name='order_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='completedorder',
            name='address_line_2',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='completedorder',
            name='notes',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='completedorder',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pendingpaymentorder',
            name='address_line_2',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='pendingpaymentorder',
            name='notes',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='pendingpaymentorder',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pullingorder',
            name='address_line_2',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='pullingorder',
            name='notes',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='pullingorder',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='readytoshiporder',
            name='address_line_2',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='readytoshiporder',
            name='notes',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='readytoshiporder',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
