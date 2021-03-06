# Generated by Django 2.2.2 on 2019-07-25 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0115_auto_20190723_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('expansion', models.CharField(default='', max_length=255)),
                ('condition', models.CharField(default='', max_length=255)),
                ('language', models.CharField(default='English', max_length=255)),
                ('foil', models.BooleanField()),
                ('sku', models.CharField(default='', max_length=255)),
                ('product_id', models.CharField(default='', max_length=255)),
                ('consecutive_days_non_direct', models.IntegerField(default=0)),
                ('total_days_non_direct', models.IntegerField(default=0)),
                ('last_add', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='updatedinventory',
            name='change_date',
            field=models.CharField(default='Wed/24/2019', max_length=255, verbose_name='Price Changed on'),
        ),
    ]
