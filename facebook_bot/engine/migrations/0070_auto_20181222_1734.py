# Generated by Django 2.1.4 on 2018-12-22 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0069_auto_20181217_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, default='', max_length=255)),
                ('expansion', models.CharField(db_index=True, default='', max_length=255)),
                ('sku', models.CharField(default='', max_length=255)),
                ('product_id', models.CharField(default='', max_length=255)),
                ('condition', models.CharField(choices=[('Near Mint', 'Near Mint'), ('Lightly Played', 'Lightly Played'), ('Moderately Played', 'Moderately Played'), ('Heavily Played', 'Heavily Played'), ('Damaged', 'Damaged')], default='Lightly Played', max_length=255)),
                ('quantity', models.IntegerField(default=0, null=True)),
                ('foil', models.BooleanField(default=False)),
                ('image', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('custom_percentage', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='updatedinventory',
            name='change_date',
            field=models.CharField(default='Sat/22/2018', max_length=255, verbose_name='Price Changed on'),
        ),
    ]
