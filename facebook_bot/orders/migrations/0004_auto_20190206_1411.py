# Generated by Django 2.1.4 on 2019-02-06 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20190206_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='address_1',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='address_2',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='city',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='country',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='email',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='first_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='last_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='postal_code',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='shipping_first_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='shipping_last_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='state',
            field=models.CharField(default='', max_length=100),
        ),
    ]
