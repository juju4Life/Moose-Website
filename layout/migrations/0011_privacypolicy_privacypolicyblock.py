# Generated by Django 3.0.5 on 2020-10-08 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layout', '0010_auto_20201007_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivacyPolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('overview', models.CharField(default='', max_length=255)),
                ('reserved_right_clause', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PrivacyPolicyBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(default='', max_length=255)),
                ('paragraph', models.TextField(default='')),
            ],
        ),
    ]