# Generated by Django 2.1.4 on 2019-01-04 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0075_auto_20181231_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='storedatabase',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='updatedinventory',
            name='change_date',
            field=models.CharField(default='Thu/03/2019', max_length=255, verbose_name='Price Changed on'),
        ),
    ]