# Generated by Django 2.2.2 on 2019-12-19 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buylist', '0026_storecredit_entries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storecredit',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]