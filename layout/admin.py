from django.contrib import admin

from .models import HomePageLayout, SinglePrintingSet, Text


@admin.register(HomePageLayout)
class HomePageAdmin(admin.ModelAdmin):
    pass


@admin.register(SinglePrintingSet)
class SinglePrintingAdmin(admin.ModelAdmin):
    search_fields = ["expansion", ]


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_filter = ['category', ]
    search_fields = ['name', ]
    list_display = ['name', 'category', ]

