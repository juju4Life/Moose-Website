# Generated by Django 2.2.2 on 2020-02-19 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20200219_1348'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customeremail',
            old_name='email_address',
            new_name='email',
        ),
    ]
