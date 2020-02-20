from django.contrib import admin
from .models import ItemizedPreorder, Customer

# Register your models here.


@admin.register(ItemizedPreorder)
class ItemPreorderAdmin(admin.ModelAdmin):
    list_display = ['name', 'expansion', 'price', 'quantity', 'available', 'total_sold']
    ordering = ['price']



