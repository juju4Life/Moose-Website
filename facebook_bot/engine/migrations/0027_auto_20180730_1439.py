# Generated by Django 2.0 on 2018-07-30 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0026_auto_20180730_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders_processing',
            name='email',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='orders_processing',
            name='order_details',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Items Ordered'),
        ),
    ]
