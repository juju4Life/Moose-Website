# Generated by Django 3.0.5 on 2020-05-04 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0160_auto_20200429_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='mtg',
            name='svg_mana_cost',
            field=models.TextField(blank=True, default=''),
        ),
    ]
