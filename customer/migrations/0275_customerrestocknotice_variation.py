# Generated by Django 3.0.5 on 2020-05-20 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0274_customerrestocknotice'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerrestocknotice',
            name='variation',
            field=models.CharField(default='', max_length=255),
        ),
    ]