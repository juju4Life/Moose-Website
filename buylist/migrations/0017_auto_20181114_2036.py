# Generated by Django 2.0 on 2018-11-15 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buylist', '0016_auto_20181114_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buying',
            name='percentage',
            field=models.DecimalField(decimal_places=0, default=0.6, max_digits=4),
        ),
    ]
