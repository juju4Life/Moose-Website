from django import forms
from engine.models import MTG


class BuylistForm(forms.ModelForm):
    name = forms.CharField()
    expansion = forms.CharField()
    buylist_price = forms.CharField()
    buylist_max_quantity = forms.IntegerField()

    class Meta:
        model = MTG
        fields = ["name", "expansion", "buylist_price", "buylist_max_quantity", ]


