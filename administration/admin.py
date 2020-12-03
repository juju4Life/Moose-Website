
from administration.models import Safe
from django.contrib import admin


@admin.register(Safe)
class SafeAdmin(admin.ModelAdmin):
    list_display = ['date_time', 'deposit', 'withdrawal', 'reason', 'manager_initials', 'balance', 'seller_name', 'notes', ]
    search_fields = ['date_time']
    list_filter = ['reason', 'date_time']
    readonly_fields = ['balance', 'date_time', ]

    fields = (
        ('deposit', 'withdrawal',),
        ('reason', 'manager_initials',),
        ('seller_name',),
        ('notes',),

    )

    # override to allow the object to be created in the admin panel while enforcing read_only fields for viewing *already created* objects only
    # Default readonly_field behavior does not allow to edit during object creation
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['deposit', 'withdrawal', 'manager_initials', ]
        return self.readonly_fields



