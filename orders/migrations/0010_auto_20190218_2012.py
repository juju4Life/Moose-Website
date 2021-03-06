# Generated by Django 2.1.4 on 2019-02-19 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20190218_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewOrders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(default='', max_length=255)),
                ('sku', models.CharField(default='', max_length=255)),
                ('name', models.CharField(default='', max_length=255)),
                ('expansion', models.CharField(default='', max_length=255)),
                ('category', models.CharField(default='', max_length=255)),
                ('condition', models.CharField(default='', max_length=255)),
                ('printing', models.CharField(default='', max_length=255)),
                ('language', models.CharField(default='', max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('quantity', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='inventory',
            name='last_sold_date',
            field=models.DateField(blank=True),
        ),
    ]
