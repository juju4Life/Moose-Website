# Generated by Django 3.0.5 on 2020-10-07 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0063_groupname_release_date'),
        ('layout', '0009_preorderitem_release_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preorderitem',
            name='release_date',
        ),
        migrations.AlterField(
            model_name='preorderitem',
            name='expansion',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.GroupName'),
        ),
    ]