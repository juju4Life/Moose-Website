from django import forms

class buylistForm(forms.Form):
    payment_info = (
        ('store_credit', 'Store Credit'),
        ('Paypal','PayPal'),
        ('check', 'Check'),
    )

    name = forms.CharField(required=False, max_length='30', help_text='Full  Name')
    email = forms.EmailField(required=True, help_text='Will be used for contact and Paypal payment')
    phone_number = forms.CharField(required=False, max_length='10')
    extension = forms.CharField(required=False, max_length='6')
    address = forms.CharField(required=True, max_length='30', help_text='Checks will be mailed to this address')
    address_2 = forms.CharField(required=False, max_length='30', help_text='address continued. apt, suite etc.')
    city = forms.CharField(required=True, max_length='15')
    state = forms.CharField(required=True, max_length='2')
    zip_code = forms.CharField(required=True)
    payment = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, choices=payment_info )
    notes = forms.CharField(required=False, widget=forms.Textarea)