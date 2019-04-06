# Generated by Django 2.1.4 on 2019-04-06 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaypalAccessToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(default='', max_length=255)),
                ('app_id', models.CharField(default='', max_length=255)),
                ('nonce', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PaypalOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(default='', max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('amount_currency_type', models.CharField(default='', max_length=255)),
                ('my_email', models.CharField(default='', max_length=255)),
                ('merchant_id', models.CharField(default='', max_length=255)),
                ('shipping_name', models.CharField(default='', max_length=255)),
                ('adress_line_1', models.CharField(default='', max_length=255)),
                ('admin_area_1', models.CharField(default='', max_length=255)),
                ('admin_area_2', models.CharField(default='', max_length=255)),
                ('postal_code', models.CharField(default='', max_length=255)),
                ('coutnry_code', models.CharField(default='', max_length=255)),
                ('payment_id', models.CharField(default='', max_length=255)),
                ('payment_status', models.CharField(default='', max_length=255)),
                ('paypal_fee', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('net', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('create_time', models.DateTimeField()),
                ('update_time', models.DateTimeField()),
                ('first_name', models.CharField(default='', max_length=255)),
                ('last_name', models.CharField(default='', max_length=255)),
                ('customer_payment_email', models.CharField(default='', max_length=255)),
                ('customer_contact_email', models.CharField(default='', max_length=255)),
                ('checkout_name', models.CharField(default='', max_length=255)),
                ('customer_id', models.CharField(default='', max_length=255)),
                ('customer_country_code', models.CharField(default='', max_length=255)),
            ],
        ),
    ]