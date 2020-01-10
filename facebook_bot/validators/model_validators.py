from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from engine.tcgplayer_api import TcgPlayerApi

api = TcgPlayerApi('first')


def validate_name(value):
    if 'x' in value:

        raise ValidationError(
            _('Name can only contain letters A-Z. Not numbers.'),
            params={'value': value},
        )


def validate_event_choice(choice):
    acceptable = ['Release Events', 'TCGplayer Kickback', 'Ban-list Update', 'Special']
    if choice not in acceptable:
        raise ValidationError(
            _('Choice cannot be None. Please choose an option.'),
            params={'choice': choice},

        )


def must_be_postive(value):
    if value < 0:
        raise ValidationError(
            _('Number must be grater than 0.')
        )


def confirm_quantity_sync(value):
    if value < 0:
        pass

    elif value > 0:
        raise ValidationError(
            _('Time to Upload.')
        )

    else:
        pass
