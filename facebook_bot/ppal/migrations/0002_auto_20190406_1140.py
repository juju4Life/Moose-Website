# Generated by Django 2.1.4 on 2019-04-06 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ppal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paypalorder',
            old_name='adress_line_1',
            new_name='address_line_1',
        ),
        migrations.RenameField(
            model_name='paypalorder',
            old_name='coutnry_code',
            new_name='country_code',
        ),
    ]
