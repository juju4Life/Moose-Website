# Generated by Django 3.0.5 on 2020-12-02 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0012_amazonpriceexclusions_price'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AmazonLiveInventory',
        ),
    ]
