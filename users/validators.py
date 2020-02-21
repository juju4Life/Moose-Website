from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


def password_needs_reset(email):
    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        user = None

    if user is not None:
        if user.has_usable_password() is False:
            raise ValidationError(_('Too many login attempts for the account associated with this email. The password needs to be reset'), code='Invalid '
                                                                                                                                              'Password')


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


def email_is_unique(email):

    if User.objects.filter(email=email).exists():

        raise ValidationError(_('An account with this email already exists.'), code='Invalid')


def month_not_blank(entry):
    if entry == '':
        raise ValidationError(_('This field cannot be blank'), code='Invalid selection')













