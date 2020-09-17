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


class BuylistPaymentType(forms.Form):
    choices = (
        ("check", "Check", ),
        ("store_credit", "Store Credit", ),
        ("paypal", "Paypal", ),
    )

    payment_type = forms.CharField(widget=forms.Select(choices=choices, attrs={"onchange": "displayPaypalEmailField()"}), )
    paypal_email = forms.EmailField(required=False)


