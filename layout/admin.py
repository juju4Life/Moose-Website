from django.contrib import admin
from layout.models import *


@ admin.register(CompanyAddress)
class CompanyAddressAdmin(admin.ModelAdmin):
    pass


@admin.register(HomePageLayout)
class HomePageAdmin(admin.ModelAdmin):
    pass


@admin.register(PreorderItem)
class PreorderAdmin(admin.ModelAdmin):
    pass


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    pass


@admin.register(PrivacyPolicyBlock)
class PrivacyPolicyBlockAdmin(admin.ModelAdmin):
    pass


@admin.register(SinglePrintingSet)
class SinglePrintingAdmin(admin.ModelAdmin):
    search_fields = ["expansion", ]


@admin.register(TermsOfService)
class TermsOfServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(TermsOfServiceBlock)
class TermsOfServiceBlockAdmin(admin.ModelAdmin):
    pass


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_filter = ['category', ]
    search_fields = ['name', ]
    list_display = ['name', 'category', ]

