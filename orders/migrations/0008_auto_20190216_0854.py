# Generated by Django 2.1.4 on 2019-02-16 13:54

from django.db import migrations, models
import validators.model_validators


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_scatterevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='scatterevent',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='scatterevent',
            name='event',
            field=models.CharField(choices=[('none', 'None'), ('release_events', 'Release Events'), ('tcgplayer_kickback', 'TCGplayer Kickback'), ('ban_list_update', 'Ban-list Update'), ('special', 'Special')], default='None', max_length=255, validators=[validators.model_validators.validate_event_choice]),
        ),
    ]
