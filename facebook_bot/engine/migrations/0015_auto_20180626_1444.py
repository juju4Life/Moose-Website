# Generated by Django 2.0 on 2018-06-26 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0014_auto_20180611_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=12, null=True),
        ),
    ]
