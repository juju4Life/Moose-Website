# Generated by Django 2.1.4 on 2019-02-20 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0090_mtg_foil'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(default='', max_length=255)),
                ('quantity', models.IntegerField(default=0)),
            ],
        ),
    ]