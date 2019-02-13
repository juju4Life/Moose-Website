from django.contrib import admin
from .models import Orders, GroupName


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    pass


admin.site.register(GroupName)

