# Generated by Django 2.2.2 on 2019-09-14 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0128_mooseautopricemetrics_sku'),
    ]

    operations = [
        migrations.AddField(
            model_name='mooseautopricemetrics',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
