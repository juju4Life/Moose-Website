# Generated by Django 3.0.5 on 2020-10-21 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0281_auto_20200911_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreCredit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('entries', models.IntegerField(default=0)),
                ('store_credit', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Credit Added')),
                ('used_credit', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Credit Used')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Store Credit History',
            },
        ),
    ]
