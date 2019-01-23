from django.db import models
from datetime import date


class Product(models.Model):
    site = models.CharField(max_length=255, default='', blank=True, null=True)
    quantity = models.IntegerField(null=True, blank=True, default=100)
    item_type = models.CharField(max_length=255, default='', blank=True, null=True)
    brand = models.CharField(max_length=255, default='', blank=True, null=True)
    specs = models.CharField(max_length=255, default='', blank=True, null=True)
    colors = models.CharField(max_length=200, default='', blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=None, null=True, blank= True)
    image = models.ImageField(null=True, blank=True, upload_to='')
    name = models.CharField(max_length=255, default='', blank=True, null=True)
    names = models.CharField(max_length=255, default='', blank=True, null=True)
    expansion = models.CharField(max_length=255, default='', blank=True, null=True)
    mana_cost = models.CharField(max_length=255, default='', blank=True, null=True)
    source = models.CharField(max_length=255, default='', blank=True, null=True)
    color_identity = models.CharField(max_length=255, default='', blank=True, null=True)
    cmc = models.CharField(max_length=255, default='', blank=True, null=True)
    types = models.CharField(max_length=255, default='', blank=True, null=True)
    supertypes = models.CharField(max_length=255, default='', blank=True, null=True)
    subtypes = models.CharField(max_length=255, default='', blank=True, null=True)
    rarity = models.CharField(max_length=255, default='', blank=True, null=True)
    text = models.TextField(default='', blank=True, null=True)
    flavor = models.TextField(default='', blank=True, null=True)
    artist = models.CharField(max_length=255, default='', blank=True, null=True)
    number = models.CharField(max_length=255, default='', blank=True, null=True)
    power = models.CharField(max_length=255, default='', blank=True, null=True)
    toughness = models.CharField(max_length=255, default='', blank=True, null=True)
    layout = models.CharField(max_length=255, default='', blank=True, null=True)
    loyalty = models.CharField(max_length=255, default='', blank=True, null=True)
    multiverse_id = models.CharField(max_length=255, default='', blank=True, null=True)
    variations = models.CharField(max_length=255, default='', blank=True, null=True)
    border = models.CharField(max_length=255, default='', blank=True, null=True)
    watermark = models.CharField(max_length=255, default='', blank=True, null=True)
    timeshifted = models.CharField(max_length=255, default='', blank=True, null=True)
    hand = models.CharField(max_length=255, default='', blank=True, null=True)
    life = models.CharField(max_length=255, default='', blank=True, null=True)
    release_date = models.CharField(max_length=255, default='', blank=True, null=True)
    starter = models.TextField(default='', blank=True, null=True)
    printings = models.TextField(default='', blank=True, null=True)
    original_text = models.TextField(default='', blank=True, null=True)
    original_type = models.CharField(max_length=255, default='', blank=True, null=True)
    image_url = models.CharField(max_length=255, default='', blank=True, null=True)
    set_name = models.CharField(max_length=255, default='', blank=True, null=True)
    card_id = models.CharField(max_length=255, default='', blank=True, null=True)
    legalities = models.TextField(default='', blank=True, null=True)
    rulings = models.TextField(default='', blank=True, null=True)
    foreign_names = models.TextField(default='', blank=True, null=True)
    tcg_player_id = models.CharField(max_length=25, default='', blank=True, null=True)

    class meta:
        indexes = [
            models.Index(fields=['set_name', 'name', 'price'])
        ]

    def __str__(self):
        return self.name



class Events(models.Model):
    title = models.CharField(max_length=255, default='')  
    game = models.CharField(max_length=255, default='')
    entry_fee = models.DecimalField(max_digits=12, decimal_places=2, default=None, blank=True)
    game_format = models.CharField(max_length=255, default='')
    description = models.TextField(default='', blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title



class StoreDatabase(models.Model):

    name = models.CharField(max_length=255, default='', db_index=True)
    expansion = models.CharField(max_length=255, default='', db_index=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    sku = models.CharField(max_length=255, default='')
    product_id = models.CharField(max_length=255, default='')
    condition = models.CharField(max_length=255, default='', db_index=True)
    quantity = models.IntegerField(null=True, default=0)
    foil = models.BooleanField(default=False)
    image = models.CharField(max_length=255, default='', blank=True, null=True)
    custom_percentage = models.IntegerField(null=True, default=0)
    language = models.CharField(max_length=255, default='', db_index=True)


    def __str__(self):
        return self.name


class MainDatabase(models.Model):

    language_choices = (
        ('english', 'English',),
        ('japanese', 'Japanese',),
        ('korean', 'Korean',),
        ('chinese (s)', 'Chinese (s)',),
        ('chinese (t)', 'Chinese (t)',),
        ('russian', 'Russian',),
        ('german', 'German',),
        ('spanish', 'Spanish',),
        ('italian', 'Italian',),
        ('french', 'French',),
        ('portuguese', 'Portuguese',),
        )

    condition_choices = (
        ('near mint', 'Near Mint',),
        ('lightly played', 'Lightly played',),
        ('moderately played', 'Moderately played',),
        ('heavily played', 'Heavily played',),
        ('damaged', 'Damaged',),
        )

    foil_choices = (
        ('non-foil', 'Non-foil',),
        ('foil', 'foil',),
        )

    name = models.CharField(max_length=150, default='', db_index=True)
    expansion = models.CharField(max_length=100, default='')
    product_id = models.CharField(max_length=12, default='')
    image = models.CharField(max_length=255, default='', blank=True, null=True)
    custom_percentage = models.IntegerField(null=True, default=0)
    
    
    
    
    
    


    

    def __str__(self):
        return self.name


class Orders(models.Model):
    order_status_type = models.CharField(max_length=50, default='', blank=True, null=True, db_index=True, verbose_name='Order Status')
    order_date = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name='Date Ordered')
    shipping_name = models.CharField(max_length=100, default='', blank=True, null=True, )
    order_number = models.CharField(max_length=50, default='', blank=True, null=True)
    order_details = models.TextField(default='', blank=True, null=True, verbose_name='Items Ordered')
    shipping_address = models.TextField(default='', blank=True, null=True)
    order_delivery_type = models.CharField(max_length=50, default='', blank=True, null=True,
                                           verbose_name='Delivery Type')
    name = models.CharField(max_length=50, default='', blank=True, null=True)
    token = models.CharField(max_length=50, default='', blank=True, null=True)
    net_profit = models.DecimalField(max_digits=12, decimal_places=2, default=None, null=True, blank=True)

    def __str__(self):
        return self.shipping_name


    class Meta:
        verbose_name_plural = "Orders"



class Sku(models.Model):
    sku = models.CharField(max_length=255, default='', blank=True, null=True, unique=True)
    name = models.CharField(max_length=255, default='', blank=True, null=True)
    expansion = models.CharField(max_length=255, default='', blank=True, null=True)
    condition = models.CharField(max_length=255, default='', blank=True, null=True)

    class meta:
        indexes = [
            models.Index(fields=['expansion', 'sku'])
        ]

    def __str__(self):
        return self.name


class ForeignOrder(models.Model):
    order_number = models.CharField(max_length=255, default='', blank=True, null=True, db_index=True)
    order_date = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name='Date Ordered')
    cards = models.TextField(default='', blank=True, null=True, verbose_name='Items Ordered')

    def __str__(self):
        return self.order_number


class TcgCredentials(models.Model):
    name = models.CharField(max_length=20, default='', blank= True)
    token = models.TextField(default='')


class UpdatedInventory(models.Model):
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='')
    condition = models.CharField(max_length=255, default='')
    is_foil = models.CharField(max_length=10, default='', verbose_name='Is it FOil?')
    previous_price = models.DecimalField(max_digits=12, decimal_places=2, default=None, null=True, blank=True, verbose_name='Previous Price')
    updated_price = models.DecimalField(max_digits=12, decimal_places=2, default=None, null=True, blank=True, verbose_name='Updated Price')
    market_price = models.DecimalField(max_digits=12, decimal_places=2, default=None, null=True, blank=True, verbose_name='Market Price')
    low_price = models.DecimalField(max_digits=12, decimal_places=2, default=None, null=True, blank=True, verbose_name='Low Price')
    mid_price = models.DecimalField(max_digits=12, decimal_places=2, default=None, null=True, blank=True, verbose_name='Mid Price')
    direct_price = models.DecimalField(max_digits=12, decimal_places=2, default=None, null=True, blank=True, verbose_name='Direct Low Price')
    change_date = models.CharField(max_length=255, default=date.today().strftime('%a/%d/%Y'), verbose_name='Price Changed on')
    sku = models.CharField(max_length=255, default='')
    group_id = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.expansion)

    class Meta:
        verbose_name_plural = "TcgPlayer Inventory Updates"



class CaseCards(models.Model):
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='')
    price = models.CharField(max_length=255, default='')
    sku = models.CharField(max_length=255, default='')
    product_id = models.CharField(max_length=255, default='')
    color = models.CharField(max_length=12, default='')
    Update_status = models.CharField(max_length=4, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Case Cards"





