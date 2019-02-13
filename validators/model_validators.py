from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_name(name):
    if not name.isalpha():
        raise ValidationError(
            _('Name can only contain letters A-Z. Not numbers.'),
            params={'name': name},
        )





