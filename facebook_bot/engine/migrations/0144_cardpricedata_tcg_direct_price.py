# Generated by Django 2.2.2 on 2019-12-31 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0143_mtg_sku_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardpricedata',
            name='tcg_direct_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12),
        ),
    ]
