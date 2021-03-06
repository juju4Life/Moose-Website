# Generated by Django 3.0.5 on 2020-09-02 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0178_auto_20200819_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='mtg',
            name='buylist',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mtg',
            name='sick_deal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mtg',
            name='sick_deal_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
