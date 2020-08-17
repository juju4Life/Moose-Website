from django.contrib import admin
from .models import FeedSubmission, AmazonPriceExclusions, AmazonLiveInventory


@admin.register(FeedSubmission)
class FeedsSubmissionAdmin(admin.ModelAdmin):
    list_display = ['feed_id', 'success', 'feed_created_on', 'feed_successful_on', ]


@admin.register(AmazonPriceExclusions)
class PricesAdmin(admin.ModelAdmin):
    search_fields = ['sku', 'name']
    ordering = ['-date_time_changed', ]
    list_filter = ["exclude", ]
    list_display = ['sku', 'min_price', 'max_price', 'exclude', 'price_metrics', 'name', 'expansion', 'condition', 'is_foil', 'date_time_changed', ]
    fields = (

        ('exclude', 'price', ),
        ('sku', 'price_metrics',),
        ('min_price', 'max_price',),
        ('is_foil', 'condition',),
        ('name', 'expansion',),
    )


@admin.register(AmazonLiveInventory)
class AmazonLiveInventoryAdmin(admin.ModelAdmin):
    pass



