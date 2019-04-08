from django.contrib import admin
from .models import PaypalAccessToken


@admin.register(PaypalAccessToken)
class PaypalCredentials(admin.ModelAdmin):
    pass
