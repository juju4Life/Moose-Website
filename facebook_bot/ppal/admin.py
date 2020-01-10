from django.contrib import admin
from .models import PaypalAccessToken, PaypalOrder


@admin.register(PaypalAccessToken)
class PaypalCredentials(admin.ModelAdmin):
    pass


@admin.register(PaypalOrder)
class PaypalOrderAdmin(admin.ModelAdmin):
    pass
