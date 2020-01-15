from django.contrib import admin
from .models import FeedSubmission, AmazonPriceExclusions, AmazonLiveInventory


@admin.register(FeedSubmission)
class FeedsSubmissionAdmin(admin.ModelAdmin):
    list_display = ['feed_id', 'success', 'feed_created_on', 'feed_successful_on', ]


@admin.register(AmazonPriceExclusions)
class PricesAdmin(admin.ModelAdmin):
    search_fields = ['sku', 'name']
    ordering = ['-exclude']
    list_display = ['sku', 'exclude', 'price_metrics', 'name', 'expansion', 'condition', 'is_foil']
    fields = (
        'exclude',
        'price_metrics',
        ('is_foil', 'condition',),
        ('sku', 'price',),
        ('name', 'expansion',),
    )


@admin.register(AmazonLiveInventory)
class AmazonLiveInventoryAdmin(admin.ModelAdmin):
    pass


