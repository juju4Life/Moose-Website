# Generated by Django 3.0.5 on 2020-09-28 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0183_auto_20200925_2030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mtg',
            old_name='hotlist',
            new_name='normal_hotlist',
        ),
        migrations.RenameField(
            model_name='mtg',
            old_name='hotlist_price',
            new_name='normal_hotlist_price',
        ),
        migrations.AddField(
            model_name='mtg',
            name='foil_hotlist',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mtg',
            name='foil_hotlist_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]