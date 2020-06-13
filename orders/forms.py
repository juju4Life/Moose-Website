from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from orders.models import ShippingMethod


class InventoryForm(forms.ModelForm):
    class Meta:
        model = []
        fields = ['name']

        def sync_check(self, instance):
            if 1 == 1:
                raise ValidationError(
                    _('Error!!')
                )

