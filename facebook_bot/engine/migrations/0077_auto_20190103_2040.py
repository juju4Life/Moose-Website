# Generated by Django 2.1.4 on 2019-01-04 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0076_auto_20190103_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storedatabase',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True),
        ),
    ]
