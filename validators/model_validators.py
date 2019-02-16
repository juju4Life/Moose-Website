from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_name(name):

    if name.isalpha() is False:
        raise ValidationError(
            _('Name can only contain letters A-Z. Not numbers.'),
            params={'na'
                    'me': name},
        )


def validate_event_choice(choice):
    acceptable = ['Release Events', 'TCGplayer Kickback', 'Ban-list Update', 'Special']
    if choice not in acceptable:
        raise ValidationError(
            _('Choice cannot be None. Please choose an option.'),
            params={'choice': choice},

        )





