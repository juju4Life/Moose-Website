from django import forms


class ContactForm(forms.Form):
    subjects = (
        ('', '', ),
        ('Order', 'I have a question about an order', ),
        ('Product', 'I have a question about a product', ),
        ('Buylist', 'I have a question about selling an item(s)', ),
        ('Other', 'I have question about something not listed above', ),
    )

    name = forms.CharField(required=True, max_length='100')
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True, widget=forms.Select(choices=subjects))
    order_number = forms.CharField(max_length=15, required=False, help_text='If applicable')
    comment = forms.CharField(required=True, widget=forms.Textarea)

    field_order = ['subject', 'name', 'email', 'order_number', 'comment']


