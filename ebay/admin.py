from django.contrib import admin
from .models import EbayAccessToken, EbayListing

# Register your models here.


@admin.register(EbayAccessToken)
class EbayTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(EbayListing)
class EbayListingAdmin(admin.ModelAdmin):
    pass
