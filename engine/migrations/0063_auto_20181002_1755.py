# Generated by Django 2.0 on 2018-10-02 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0062_auto_20180922_1237'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='casecards',
            options={'verbose_name_plural': 'Case Cards'},
        ),
        migrations.AlterModelOptions(
            name='updatedinventory',
            options={'verbose_name_plural': 'TcgPlayer Inventory Updates'},
        ),
        migrations.AlterField(
            model_name='updatedinventory',
            name='change_date',
            field=models.CharField(default='Tue/02/2018', max_length=255, verbose_name='Price Changed on'),
        ),
    ]
