# Generated by Django 3.0.5 on 2020-06-20 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0046_orderslayout'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderslayout',
            name='label',
            field=models.CharField(default='', max_length=255),
        ),
    ]