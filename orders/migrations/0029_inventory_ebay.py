# Generated by Django 2.1.4 on 2019-03-20 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0028_auto_20190311_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='ebay',
            field=models.BooleanField(default=False, verbose_name='On eBay'),
        ),
    ]
