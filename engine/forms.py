from django import forms

class contactForm(forms.Form):
    condition_choice = (
        ('near mint / lightly played', 'Near Mint / Lightly Played'),
        ('played / moderately played', 'Played / Moderately Played'),
        ('heavily played', 'Heavily Played'),
    )

    yes_no = (
        ('yes', 'Yes'),
        ('no', 'No')
    )

    contact_choice = (
        ('email', 'Email'),
        ('text message', 'Text Message'),
        ('phone call', ' Phone Call'),
        ('i am present in-store', ' I am present in-store'),
    )

    name = forms.CharField(required=True, max_length='30')
    contact_type = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, choices=contact_choice,
                                             label='How would you like to be contacted?')
    email = forms.EmailField(required=False,label='Email - (if Contact by Email selected)')
    phone_number = forms.CharField(required=False, max_length='15', label='Phone Number - (if Contact by Phone selected)')
    notes = forms.CharField(required=False, widget=forms.Textarea)