from django.contrib import admin
from .models import Orders, GroupName


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    change_list_template = 'admin/sale_summary_change_list.html'


admin.site.register(GroupName)

