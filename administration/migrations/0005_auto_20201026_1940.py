# Generated by Django 3.0.5 on 2020-10-26 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0004_auto_20201026_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='safe',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='safe',
            name='reason',
            field=models.CharField(choices=[('', ''), ('daily_deposit', 'daily deposit'), ('drawer_balance', 'drawer balance'), ('other_payment', 'other payment'), ('restock', 'safe restock'), ('safe_balance', 'safe balance'), ('trade_in', 'trade in')], default='', max_length=255),
        ),
    ]
