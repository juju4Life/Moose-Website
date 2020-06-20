from django.db import models


class CardPriceData(models.Model):
    c = (
        ('yes', 'Yes',),
        ('no', 'No',),
    )

    sku = models.CharField(max_length=255, default='', blank=True)
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='', blank=True)
    product_id = models.CharField(max_length=255, default='', blank=True)
    tcg_direct_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    direct_net = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    tcg_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    tcg_market = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    tcg_net = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    amazon_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    amazon_net = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    scg_buylist = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    ck_buylist = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    cfb_buylist = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    low_store_stock = models.CharField(max_length=3, default='No', choices=c)
    store_quantity_needed = models.IntegerField(default=0)
    printing = models.CharField(max_length=255, default='')
    sell_to = models.CharField(max_length=255, default='')
    best_net = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class MooseAutopriceMetrics(models.Model):
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='')
    condition = models.CharField(max_length=255, default='')
    printing = models.CharField(max_length=255, default='')
    language = models.CharField(max_length=255, default='')
    sku = models.CharField(max_length=255, default='')
    updated_price = models.CharField(max_length=255, default='')
    updated_at = models.DateTimeField(auto_now=True)
    old_price = models.CharField(max_length=255, default='')
    price_1 = models.CharField(max_length=255, default='')
    price_1_gold = models.BooleanField(default=False, blank=True)
    price_2 = models.CharField(max_length=255, default='', blank=True)
    price_2_gold = models.BooleanField(default=False, blank=True)
    price_3 = models.CharField(max_length=255, default='', blank=True)
    price_3_gold = models.BooleanField(default=False)
    price_4 = models.CharField(max_length=255, default='', blank=True)
    price_4_gold = models.BooleanField(default=False, blank=True)
    price_5 = models.CharField(max_length=255, default='', blank=True)
    price_5_gold = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.name}({self.expansion})'


class MooseInventory(models.Model):
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='')
    condition = models.CharField(max_length=255, default='')
    printing = models.CharField(max_length=255, default='')
    seller_1_name = models.CharField(max_length=255, default='')
    seller_1_total_sales = models.CharField(max_length=255, default='')
    seller_1_total_price = models.CharField(max_length=255, default='')
    seller_2_name = models.CharField(max_length=255, default='')
    seller_2_total_sales = models.CharField(max_length=255, default='')
    seller_2_total_price = models.CharField(max_length=255, default='')
    updated_price = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class TcgGroupPrice(models.Model):
    product_id = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='')
    printing = models.CharField(max_length=255, default='')
    low_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mid_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    market_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    high_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    direct_low_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_direct = models.BooleanField(default=False)
    price_history = models.TextField(default='')

    def __str__(self):
        return self.name


class DirectData(models.Model):
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='')
    condition = models.CharField(max_length=255, default='')
    language = models.CharField(max_length=255, default='English')
    foil = models.BooleanField()
    sku = models.CharField(max_length=255, default='')
    product_id = models.CharField(max_length=255, default='')
    consecutive_days_non_direct = models.IntegerField(default=1)
    total_days_non_direct = models.IntegerField(default=1)
    last_add = models.DateField(verbose_name="Last Non-direct Date")
    last_consecutive_run = models.IntegerField(default=1)
    days_non_direct = models.IntegerField(default=1)
    in_stock = models.BooleanField(default=False)
    current_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    market = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    low = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)

    def __str__(self):
        return self.name


class MtgCardInfo(models.Model):
    name = models.CharField(max_length=255, default='')
    card_identifier = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class MTG(models.Model):
    name = models.CharField(max_length=255, default='', verbose_name='name', db_index=True)
    expansion = models.CharField(max_length=255, default='', db_index=True)
    product_id = models.CharField(max_length=30, default='')
    image_url = models.CharField(max_length=255, default='')
    language = models.CharField(max_length=255, default='English')

    normal_clean_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    normal_clean_stock = models.IntegerField(default=0)
    normal_played_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    normal_played_stock = models.IntegerField(default=0)
    normal_heavily_played_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    normal_heavily_played_stock = models.IntegerField(default=0)
    foil_clean_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    foil_clean_stock = models.IntegerField(default=0)
    foil_played_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    foil_played_stock = models.IntegerField(default=0)
    foil_heavily_played_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    foil_heavily_played_stock = models.IntegerField(default=0)

    set_abbreviation = models.CharField(max_length=255, default='', blank=True)
    rarity = models.CharField(max_length=255, default='', blank=True)
    oracle_text = models.TextField(default='', blank=True)
    flavor_text = models.TextField(default='', blank=True)
    colors = models.CharField(max_length=255, default='', blank=True)
    color_identity = models.CharField(max_length=255, default='', blank=True)
    card_type = models.CharField(max_length=255, default='', blank=True)
    subtypes = models.CharField(max_length=255, default='', blank=True)
    loyalty = models.CharField(max_length=255, default='', blank=True)
    power = models.CharField(max_length=255, null=True, default=None, blank=True)
    toughness = models.CharField(max_length=255, null=True, default=None, blank=True)
    layout = models.CharField(max_length=255, default='', blank=True)
    artist = models.CharField(max_length=255, default='', blank=True)
    collector_number = models.CharField(max_length=255, default='', blank=True)
    mana_cost = models.CharField(max_length=255, default='', blank=True)
    mana_cost_encoded = models.CharField(max_length=255, default='', blank=True)
    converted_mana_cost = models.DecimalField(max_digits=10, decimal_places=1, null=True, default=None, blank=True)
    converted = models.BooleanField(default=False)

    restock_notice = models.ManyToManyField("customer.CustomerRestockNotice")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "MTG Card Database"
        ordering = ['expansion', 'name']


class TcgCredentials(models.Model):
    name = models.CharField(max_length=20, default='', blank=True)
    token = models.TextField(default='')





