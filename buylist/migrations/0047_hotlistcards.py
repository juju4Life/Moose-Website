# Generated by Django 3.0.5 on 2020-10-30 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0189_mtg_release_date'),
        ('buylist', '0046_delete_storecredit'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotListCards',
            fields=[
                ('mtg_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='engine.MTG')),
            ],
            options={
                'abstract': False,
            },
            bases=('engine.mtg',),
        ),
    ]
