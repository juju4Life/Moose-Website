# Generated by Django 2.0 on 2018-09-22 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buylist', '0012_auto_20180921_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buying',
            name='sku',
            field=models.CharField(default='None', max_length=255),
        ),
    ]
