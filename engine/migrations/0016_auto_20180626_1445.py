# Generated by Django 2.0 on 2018-06-26 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0015_auto_20180626_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
