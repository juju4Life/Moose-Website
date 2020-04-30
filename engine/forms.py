from django import forms


class AdvancedSearchForm(forms.Form):

    color_option_choices = (
        ("include_colorless", " include colorless cards"),
        ("include_mono_color", " include mono-color cards"),
        ("include_multi_color", " include all multi-color cards"),
        (2, " 2-color cards"),
        (3, " 3-color cards"),
        (4, " 4-color cards"),
        (5, " 5-color cards"),
    )

    name_choices = (
        ("contains", " contains", ),
        ("equals", " equal to", ),
    )

    color_choices = (
        ("B", " Black",),
        ("G", " Green",),
        ("R", " Red",),
        ("U", " Blue",),
        ("W", " White",),
    )

    rarity_choices = (
        ("M", " Mythic",),
        ("R", " Rare",),
        ("U", " Uncommon",),
        ("C", " Common",),
    )

    card_type_choices = (
        ("Artifact", " Artifact", ),
        ("Creature", " Creature", ),
        ("Enchantment", " Enchantment", ),
        ("Instant", " Instant", ),
        ("Land", "Land", ),
        ("Legendary", " Legendary", ),
        ("Planeswalker", " Planeswalker", ),
        ("Sorcery", " Sorcery", ),
        ("Tribal", " Tribal", ),
    )

    oracle_text = forms.CharField(widget=forms.TextInput(attrs={
        "class": "advanced-search-form form-control",
    }), label='', required=False)

    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "advanced-search-form form-control",
    }), label='', required=False)

    name_query = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=name_choices,
        label='',
        required=False,
    )

    expansion = forms.CharField(widget=forms.TextInput(attrs={"class": "advanced-search-form form-control", "id": "advanced-search-form-expansion"}), label="",
                                required=False)

    artist = forms.CharField(widget=forms.TextInput(attrs={"class": "advanced-search-form form-control", "id": "advanced-search-form-card-artist"}), label="",
                             required=False)

    color_options = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=color_option_choices,
        label='',
        required=False,

    )

    colors = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input", "type": "checkbox"}),
        choices=color_choices,
        label='',
        required=False,
    )

    color_identity = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=color_choices,
        label='',
        required=False,
    )

    rarity = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=rarity_choices,
        label='',
        required=False,
    )

    card_type = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={"id": "advanced-search-form-card-type"}),
        choices=card_type_choices,
        label='',
        required=False,
    )

    subtypes = forms.CharField(widget=forms.TextInput(attrs={
        "class": "advanced-search-form form-control", "id": "advanced-search-form-subtypes"}),
         label='', required=False
    )

    power_start = forms.IntegerField(widget=forms.TextInput(attrs={
        "class": "advanced-search-form form-control"}), label='', required=False)

    power_end = forms.IntegerField(widget=forms.TextInput(attrs={
        "class": "advanced-search-form form-control"}), label='', required=False)

    toughness_start = forms.IntegerField(widget=forms.TextInput(attrs={
        "class": "advanced-search-form form-control"}), label='', required=False)

    toughness_end = forms.IntegerField(widget=forms.TextInput(attrs={
        "class": "advanced-search-form form-control"}), label='', required=False)

    cmc_start = forms.IntegerField(widget=forms.TextInput(attrs={
        "class": "advanced-search-form form-control"}), label='', required=False)

    cmc_end = forms.IntegerField(widget=forms.TextInput(attrs={
        "class": "advanced-search-form form-control"}), label="", required=False)


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


