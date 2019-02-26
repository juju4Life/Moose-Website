# Generated by Django 2.1.4 on 2019-02-26 15:15

from django.db import migrations, models
import validators.model_validators


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_auto_20190219_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='update_choice_quantity',
            field=models.IntegerField(default=0, validators=[validators.model_validators.must_be_postive]),
        ),
        migrations.AddField(
            model_name='inventory',
            name='update_item',
            field=models.CharField(choices=[('none', 'none'), ('remove', 'Remove'), ('upload', 'Upload')], default='none', max_length=100),
        ),
    ]
