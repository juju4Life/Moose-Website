# Generated by Django 2.0 on 2018-09-21 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0060_auto_20180919_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updatedinventory',
            name='change_date',
            field=models.CharField(default='Fri/21/2018', max_length=255, verbose_name='Price Changed on'),
        ),
    ]
