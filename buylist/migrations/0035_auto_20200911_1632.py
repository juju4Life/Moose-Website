# Generated by Django 3.0.5 on 2020-09-11 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buylist', '0034_buylistsubmission_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buylistsubmission',
            name='buylist_number',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='buylistsubmission',
            name='buylist_status',
            field=models.CharField(default='Not Received', max_length=255),
        ),
    ]