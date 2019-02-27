from django import forms
from .models import Inventory
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name']

        def sync_check(self, instance):
            if 1 == 1:
                raise ValidationError(
                    _('Error!!')
                )




