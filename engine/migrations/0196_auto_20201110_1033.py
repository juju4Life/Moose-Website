# Generated by Django 3.0.5 on 2020-11-10 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0195_auto_20201109_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardpricedata',
            name='product_id',
            field=models.CharField(blank=True, default='', max_length=255, unique=True),
        ),
    ]
