# Generated by Django 2.2.2 on 2019-09-13 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0126_mooseautopricemetrics'),
    ]

    operations = [
        migrations.AddField(
            model_name='mooseautopricemetrics',
            name='language',
            field=models.CharField(default='', max_length=255),
        ),
    ]