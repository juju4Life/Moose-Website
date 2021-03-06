# Generated by Django 2.0 on 2018-09-15 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0054_updatedinventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='updatedinventory',
            name='direct_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=12, null=True, verbose_name='Direct Low Price'),
        ),
        migrations.AddField(
            model_name='updatedinventory',
            name='low_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=12, null=True, verbose_name='Low Price'),
        ),
        migrations.AddField(
            model_name='updatedinventory',
            name='market_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=12, null=True, verbose_name='Market Price'),
        ),
        migrations.AddField(
            model_name='updatedinventory',
            name='mid_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=12, null=True, verbose_name='Mid Price'),
        ),
        migrations.AlterField(
            model_name='updatedinventory',
            name='is_foil',
            field=models.CharField(default='', max_length=10, verbose_name='Is it FOil?'),
        ),
    ]
