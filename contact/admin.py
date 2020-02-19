from django.contrib import admin
from .models import CustomerEmail


@admin.register(CustomerEmail)
class CustomerEmailAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'message', 'subject', 'message_created_at', 'replied_at', 'order_number', 'email']
    exclude = ['uuid']

