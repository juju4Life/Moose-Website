# Generated by Django 3.0.5 on 2020-10-26 20:44

from django.db import migrations, models
import validators.model_validators


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='safe',
            name='deposit',
            field=models.CharField(default='0', max_length=12, validators=[validators.model_validators.contains_plus]),
        ),
        migrations.AlterField(
            model_name='safe',
            name='withdrawal',
            field=models.CharField(default='0', max_length=12, validators=[validators.model_validators.contains_minus]),
        ),
    ]
