# Generated by Django 2.2.2 on 2019-10-19 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0134_auto_20190928_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='mtg',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]