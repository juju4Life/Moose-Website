from django.contrib import admin

from .models import HomePageLayout, SinglePrintingSet


@admin.register(HomePageLayout)
class HomePageAdmin(admin.ModelAdmin):
    pass


@admin.register(SinglePrintingSet)
class SinglePrintingAdmin(admin.ModelAdmin):
    search_fields = ["expansion", ]


