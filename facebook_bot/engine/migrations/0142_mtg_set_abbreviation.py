# Generated by Django 2.2.2 on 2019-11-30 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0141_auto_20191130_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='mtg',
            name='set_abbreviation',
            field=models.CharField(db_index=True, default='', max_length=255),
        ),
    ]
