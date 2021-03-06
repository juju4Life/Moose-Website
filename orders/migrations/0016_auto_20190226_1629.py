# Generated by Django 2.1.4 on 2019-02-26 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20190226_1128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventory',
            options={'verbose_name_plural': 'Inventory'},
        ),
        migrations.AlterModelOptions(
            name='neworders',
            options={'verbose_name_plural': 'Ordered Singles'},
        ),
        migrations.AlterField(
            model_name='inventory',
            name='printing',
            field=models.CharField(default='', max_length=255, verbose_name='Foil'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='update_inventory_quantity',
            field=models.IntegerField(default=0),
        ),
    ]
