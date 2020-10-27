
from administration.models import Safe
from django.contrib import admin


@admin.register(Safe)
class SafeAdmin(admin.ModelAdmin):
    list_display = ['date_time', 'deposit', 'withdrawal', 'reason', 'manager_initials', 'balance', 'seller_name', 'notes', ]
    search_fields = ['date_time']
    list_filter = ['reason', 'date_time']
    readonly_fields = ['balance', 'date_time', ]
    fields = (
        ('deposit', 'withdrawal', ),
        ('reason', 'manager_initials', ),
        ('seller_name', ),
        ('notes', ),

    )


