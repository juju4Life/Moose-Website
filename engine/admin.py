from time import localtime, strftime

from django.contrib import admin
from django.contrib.auth.models import Group

from engine.models import MTG, DirectData, TcgGroupPrice, MooseInventory, MooseAutopriceMetrics, CardPriceData
from engine.tcgplayer_api import TcgPlayerApi

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field


api = TcgPlayerApi('first')

# TcgPlayer Buylist Hub --------------------------------------------------------------------------------------------------------------------


class CardDataResource(resources.ModelResource):

    name = Field(attribute='name', column_name='Name')
    expansion = Field(attribute='expansion', column_name='Set')
    tcg_net = Field(attribute='tcg_net', column_name='Tcg Net')
    tcg_price = Field(attribute='tcg_price', column_name='Tcg Price')
    tcg_market = Field(attribute='tcg_market', column_name='Tcg Market')
    amazon_price = Field(attribute='amazon_price', column_name='Amazon Price')
    amazon_net = Field(attribute='amazon_net', column_name='Amazon Net')
    scg_buylist = Field(attribute='scg_buylist', column_name='SCG Buylist')
    ck_buylist = Field(attribute='ck_buylist', column_name='CK Buylist')

    class Meta:
        model = CardPriceData
        exclude = ('id', 'cfb_buylist', 'direct_net', 'store_quantity_needed', 'printing', 'sell_to', 'best_net',
                   'sku', 'product_id', 'tcg_direct_price', 'updated', )


@admin.register(CardPriceData)
class CardPriceAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'expansion', 'ck_buylist', 'scg_buylist', 'tcg_direct_price', 'tcg_price', 'amazon_price', 'low_store_stock',
                    'store_quantity_needed', 'sell_to', 'updated', ]
    ordering = ['name']
    resource_class = CardDataResource
# TcgPlayer Buylist Hub END --------------------------------------------------------------------------------------------------------------------


# Moose Tcg Auto Price Metrics ----------------- START
@admin.register(MooseAutopriceMetrics)
class MooseMetricsAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['old_price', 'updated_price', 'name', 'expansion', 'condition', 'printing', 'updated_at',
                    'price_1', 'price_1_gold',
                    'price_2', 'price_2_gold',
                    'price_3', 'price_3_gold',
                    'price_4', 'price_4_gold',
                    'price_5', 'price_5_gold', ]
# Moose Tcg Auto Pricer Metrics ----------------- END


@admin.register(MooseInventory)
class MooseInv(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'expansion', 'condition', 'updated_price']


# Magic the Gathering Card Database ------------------ START
class MTGResource(resources.ModelResource):
    product_id = Field(attribute='product_id', column_name='Id')
    name = Field(attribute='name', column_name='Name')
    normal_clean_stock = Field(attribute='normal_clean_stock', column_name='Normal Clean')
    normal_played_stock = Field(attribute='normal_played_stock', column_name='Normal Played')
    normal_heavily_played_stock = Field(attribute='normal_heavily_played_stock', column_name='Normal Heavy')
    foil_clean_stock = Field(attribute='foil_clean_stock', column_name='Foil Clean')
    foil_played_stock = Field(attribute='foil_played_stock', column_name='Foil Played')
    foil_heavily_played_stock = Field(attribute='foil_heavily_played_stock', column_name='Foil Heavy')

    class Meta:
        model = MTG
        fields = ('product_id', 'name', 'normal_clean_stock', 'normal_played_stock', 'normal_heavily_played_stock',
                  'foil_clean_stock', 'foil_played_stock', 'foil_heavily_played_stock',)
        exclude = ('language', )
        import_id_fields = ('product_id',)


@admin.register(MTG)
class MTGAdmin(ImportExportModelAdmin):
    def get_export_filename(self, request, queryset, file_format):
        date_time = strftime("%Y-%m-%d %I_%M%p", localtime())
        filename = f"{queryset[0].expansion} - {date_time}.csv"

        return filename

    resource_class = MTGResource
    search_fields = ['name']
    list_display = ['name', 'expansion', 'language', ]
    list_filter = ['expansion']
    fields = (
        "svg_mana_cost",
        ("name", "expansion", ),
        ("language", ),
        ("normal_clean_price", "normal_clean_stock", ),
        ("normal_played_price", "normal_played_stock", ),
        ("normal_heavily_played_price", "normal_heavily_played_stock", ),
        ("foil_clean_price", "foil_clean_stock",),
        ("foil_played_price", "foil_played_stock",),
        ("foil_heavily_played_price", "foil_heavily_played_stock",),
    )
# Magic the Gathering Card Database ------------------ END


@admin.register(TcgGroupPrice)
class TcgGroupPriceAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    list_display = ['name', 'expansion', 'direct_low_price', 'market_price', 'low_price', 'mid_price', 'printing', ]


@admin.register(DirectData)
class DirectTrackerAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'expansion', 'consecutive_days_non_direct', 'total_days_non_direct', 'condition', 'foil', 'last_add', 'in_stock',
                    'current_price', 'low', 'market', ]
    ordering = ['-in_stock', '-last_add', '-consecutive_days_non_direct']


admin.site.site_header = 'MooseLoot'
admin.site.site_title = ''
admin.site.index_title = 'MooseLoot'
admin.site.unregister(Group)
