# Generated by Django 3.0.5 on 2020-06-30 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0051_auto_20200629_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address_line_2',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
