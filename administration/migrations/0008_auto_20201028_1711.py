# Generated by Django 3.0.5 on 2020-10-28 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0007_auto_20201026_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='safe',
            name='alert',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='safe',
            name='reason',
            field=models.CharField(choices=[('', ''), ('mtg_trade_in', 'mtg trade'), ('pokemon_trade_in', 'pokemon trade'), ('yugioh_trade_in', 'yugioh trade'), ('trade_in', 'trade in'), ('daily_deposit', 'daily deposit'), ('drawer_balance', 'drawer balance'), ('other_purchase', 'other purchase'), ('safe_restock', 'safe restock'), ('safe_balance', 'safe balance')], default='', max_length=255),
        ),
    ]
