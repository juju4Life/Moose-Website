# Generated by Django 3.0.5 on 2020-11-09 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0192_sickdeal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tcggroupprice',
            name='high_price',
        ),
        migrations.RemoveField(
            model_name='tcggroupprice',
            name='is_direct',
        ),
        migrations.RemoveField(
            model_name='tcggroupprice',
            name='price_history',
        ),
    ]