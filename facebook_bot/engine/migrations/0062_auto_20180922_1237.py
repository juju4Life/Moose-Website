# Generated by Django 2.0 on 2018-09-22 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0061_auto_20180921_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updatedinventory',
            name='change_date',
            field=models.CharField(default='Sat/22/2018', max_length=255, verbose_name='Price Changed on'),
        ),
    ]
