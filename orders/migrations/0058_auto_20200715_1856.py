# Generated by Django 3.0.5 on 2020-07-15 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0057_order_order_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='completedorder',
            name='order_action',
            field=models.CharField(blank=True, choices=[('', ''), ('cancel', 'cancel'), ('pull', 'Move to Pulling'), ('ship', 'Mark as Shipped')], default='', max_length=255),
        ),
        migrations.AddField(
            model_name='pendingpaymentorder',
            name='order_action',
            field=models.CharField(blank=True, choices=[('', ''), ('cancel', 'cancel'), ('pull', 'Move to Pulling'), ('ship', 'Mark as Shipped')], default='', max_length=255),
        ),
        migrations.AddField(
            model_name='pullingorder',
            name='order_action',
            field=models.CharField(blank=True, choices=[('', ''), ('cancel', 'cancel'), ('pull', 'Move to Pulling'), ('ship', 'Mark as Shipped')], default='', max_length=255),
        ),
        migrations.AddField(
            model_name='readytoshiporder',
            name='order_action',
            field=models.CharField(blank=True, choices=[('', ''), ('cancel', 'cancel'), ('pull', 'Move to Pulling'), ('ship', 'Mark as Shipped')], default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_action',
            field=models.CharField(blank=True, choices=[('', ''), ('cancel', 'cancel'), ('pull', 'Move to Pulling'), ('ship', 'Mark as Shipped')], default='', max_length=255),
        ),
    ]
