from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_zip_code(zip_code):
    errors = []

    if not zip_code.isnumeric():
        errors.append(
            ValidationError(_('Must use numeric characters only.'), code='Zip Code not Numeric')
        )

    if len(zip_code) < 5:
        errors.append(
            ValidationError(_('Cannot be less than 5 characters.'), code='Zip Code too short')
        )

    if errors:
        raise ValidationError(
            errors
        )













