# Generated by Django 2.2.2 on 2019-11-30 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0139_auto_20191125_2015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mtg',
            name='number',
        ),
        migrations.RemoveField(
            model_name='mtg',
            name='product_line',
        ),
        migrations.RemoveField(
            model_name='mtg',
            name='title',
        ),
        migrations.AddField(
            model_name='mtg',
            name='artist',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='mtg',
            name='collector_number',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='mtg',
            name='color_identity',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='mtg',
            name='colors',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='mtg',
            name='converted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mtg',
            name='converted_mana_cost',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='mtg',
            name='flavor_text',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='mtg',
            name='layout',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='mtg',
            name='loyalty',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='mtg',
            name='mana_cost',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='mtg',
            name='oracle_text',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='mtg',
            name='power',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='mtg',
            name='toughness',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
