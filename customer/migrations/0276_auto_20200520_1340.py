# Generated by Django 3.0.5 on 2020-05-20 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0275_customerrestocknotice_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='restock_notice',
        ),
        migrations.RemoveField(
            model_name='historicalcustomer',
            name='restock_notice',
        ),
        migrations.AddField(
            model_name='customer',
            name='restock_list',
            field=models.ManyToManyField(to='customer.CustomerRestockNotice'),
        ),
    ]
