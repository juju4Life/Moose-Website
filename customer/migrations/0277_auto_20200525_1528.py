# Generated by Django 3.0.5 on 2020-05-25 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0276_auto_20200520_1340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerrestocknotice',
            name='variation',
        ),
        migrations.AddField(
            model_name='customerrestocknotice',
            name='expansion',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='customerrestocknotice',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
