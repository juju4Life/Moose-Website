# Generated by Django 3.0.5 on 2020-09-28 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buylist', '0041_hotlist_printing'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardkingdombuylist',
            name='product_id',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='starcitybuylist',
            name='product_id',
            field=models.CharField(default='', max_length=255),
        ),
    ]