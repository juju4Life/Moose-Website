from django.db import models


class CardPriceData(models.Model):
    sku = models.CharField(max_length=255, default='', blank=True)
    name = models.CharField(max_length=255, default='')
    expansion = models.CharField(max_length=255, default='', blank=True)
    product_id = models.CharField(max_length=255, default='', blank=True)
    tcg_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    tcg_net = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    amazon_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    amazon_net = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    scg_buylist = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    ck_buylist = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    cfb_buylist = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)

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
    price_1_gold = models.BooleanField(default=False)
    price_2 = models.CharField(max_length=255, default='')
    price_2_gold = models.BooleanField(default=False)
    price_3 = models.CharField(max_length=255, default='')
    price_3_gold = models.BooleanField(default=False)
    price_4 = models.CharField(max_length=255, default='')
    price_4_gold = models.BooleanField(default=False)
    price_5 = models.CharField(max_length=255, default='')
    price_5_gold = models.BooleanField(default=False)

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
    foil = models.BooleanField(default=False)
    low_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mid_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    market_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    high_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    direct_low_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_direct = models.BooleanField(default=False)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class MTG(models.Model):
    product_name = models.CharField(max_length=255, default='', db_index=True, verbose_name='name')
    product_line = models.CharField(max_length=255, default='')
    title = models.CharField(max_length=255, default='')
    rarity = models.CharField(max_length=255, default='')
    number = models.CharField(max_length=255, default='')
    set_name = models.CharField(max_length=255, default='', db_index=True)
    sku = models.CharField(max_length=255, default='')
    condition = models.CharField(max_length=255, default='', db_index=True)
    language = models.CharField(max_length=255, default='English', db_index=True)
    foil = models.BooleanField(default=False)
    product_id = models.CharField(max_length=30, default='')
    image_url = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.product_name


class MtgForeign(models.Model):
    product_name = models.CharField(max_length=255, default='', db_index=True, verbose_name='name')
    product_line = models.CharField(max_length=255, default='')
    title = models.CharField(max_length=255, default='')
    rarity = models.CharField(max_length=255, default='')
    number = models.CharField(max_length=255, default='')
    set_name = models.CharField(max_length=255, default='', db_index=True)
    sku = models.CharField(max_length=255, default='')
    condition = models.CharField(max_length=255, default='', db_index=True)
    language = models.CharField(max_length=255, default='Unknown', db_index=True)
    foil = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name


class Yugioh(models.Model):
    product_name = models.CharField(max_length=255, default='', db_index=True, verbose_name='name')
    product_line = models.CharField(max_length=255, default='')
    title = models.CharField(max_length=255, default='')
    rarity = models.CharField(max_length=255, default='')
    number = models.CharField(max_length=255, default='')
    set_name = models.CharField(max_length=255, default='', db_index=True)
    sku = models.CharField(max_length=255, default='')
    condition = models.CharField(max_length=255, default='', db_index=True)
    language = models.CharField(max_length=255, default='English', db_index=True)
    foil = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name


class Pokemon(models.Model):
    product_name = models.CharField(max_length=255, default='', db_index=True, verbose_name='name')
    product_line = models.CharField(max_length=255, default='')
    title = models.CharField(max_length=255, default='')
    rarity = models.CharField(max_length=255, default='')
    number = models.CharField(max_length=255, default='')
    set_name = models.CharField(max_length=255, default='', db_index=True)
    sku = models.CharField(max_length=255, default='')
    condition = models.CharField(max_length=255, default='', db_index=True)
    language = models.CharField(max_length=255, default='English', db_index=True)
    foil = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name


class Upload(models.Model):
    sku = models.CharField(max_length=255, default='')
    upload_status = models.BooleanField(default=False)
    name = models.CharField(max_length=255, default='')
    group_name = models.CharField(max_length=255, default='')
    condition = models.CharField(max_length=255, default='')
    printing = models.CharField(max_length=255, default='', verbose_name='Foil')
    language = models.CharField(max_length=255, default='')
    category = models.CharField(max_length=255, default='')
    upload_quantity = models.IntegerField(default=0)
    upload_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    upload_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.sku

    class Meta:
        verbose_name_plural = "Upload"


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


class TcgCredentials(models.Model):
    name = models.CharField(max_length=20, default='', blank=True)
    token = models.TextField(default='')





