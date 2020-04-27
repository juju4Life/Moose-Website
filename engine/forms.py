from django import forms


class AdvancedSearchForm(forms.Form):
    name_choices = (
        ("", "", ),
        ("contains", "contains", ),
        ("equals", "equals", ),
    )

    color_choices = (
        ("", "",),
        ("colorless", "colorless",),
        ("black", "black",),
        ("blue", "blue",),
        ("green", "green",),
        ("red", "red",),
        ("white", "white",),
    )
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "advanced-search-form form-control",
    }), label='')
    name_query = forms.CharField(widget=forms.Select(choices=name_choices, attrs={"class": "query-drop-down"}), label='')
    expansion = forms.CharField(widget=forms.TextInput(attrs={"class": "advanced-search-form form-control"}))

    color_query = forms.CharField(widget=forms.Select(choices=color_choices, attrs={"class": "query-drop-down"}), label='')
    color = forms.CharField(widget=forms.TextInput(attrs={"class": "advanced-search-form form-control"}))


class contactForm(forms.Form):

    yes_no = (
        ('yes', 'Yes'),
        ('no', 'No')
    )

    name = forms.CharField(required=True, max_length='30')
    email = forms.EmailField(required=True, label='Email')
    # notes = forms.CharField(required=False, widget=forms.Textarea)


class ConditionSkuForm(forms.Form):

    def __init__(self, instance, *args, **kwargs):
        self.condition_choices = (

            ('near mint', 'Near Mint / Lightly Played'),
            ('moderately played', 'Moderately Played'),
            ('heavily played', 'Heavily Played'),
            ('damaged', 'Damaged'),
        )    
        self.language_choices = (
            ('english', 'English'),
            ('japanese', 'Japanese'),
            ('chinese (s)', 'Chinese (S)'),
            ('german', 'German'),
            ('korean', 'Korean'),
            ('russian', 'Russian'),
            ('spanish', 'Spanish'),
            ('italian', 'Italian'),
            ('french', 'French'),
            ('portuguese', 'Portuguese'),
        )
        self.foil_choices = (
                ('false', 'Non-foil',),
                ('true','Foil'),
            )
        super(ConditionSkuForm, self).__init__(*args, **kwargs)
        #  self.fields['condition'].widget.attrs['id'] = instance.id

        self.fields['condition'].widget = forms.Select(choices=self.condition_choices, attrs={"id": instance.product_id, "onchange": "conditionChange(this)"})
        self.fields['language'].widget = forms.Select(choices=self.language_choices, attrs={"id": instance.product_id, "onchange": "languageChange(this)"})
        self.fields['foil'].widget = forms.Select(choices=self.foil_choices, attrs={"id": instance.product_id, "onchange": "foilChange(this)"})

    condition = forms.ChoiceField(initial='near mint')
    language = forms.ChoiceField(initial='english')
    foil = forms.ChoiceField(initial='false')
    #  quantity = forms.IntegerField(initial=1)


class ProductForm(forms.ModelForm):

    class Meta:
        model = ''
        exclude = ()
        fields = ['condition_select', 'language_select', 'foil_select']

    def __init__(self, *args, **kwargs):

        super(ProductForm, self).__init__(*args, **kwargs)
        instance = kwargs['instance']
        self.fields['condition_select'].widget.attrs['data-product_id'] = instance.product_id


