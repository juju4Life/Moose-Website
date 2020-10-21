from django.contrib import admin
from customer.models import Customer, StoreCredit
from simple_history.admin import SimpleHistoryAdmin


# Register your models here.

@admin.register(Customer)
class CustomerAdmin(SimpleHistoryAdmin):

    # ip, is_routable = get_client_ip(request)

    # alert.apply_async(que='low_priority', args=(ip, obj.name, obj.credit, obj.id,))

    save_on_top = True
    history_list_display = ['credit', 'employee_initial', 'changeReason', ]
    list_display = ['name', 'credit', 'email', 'notes', ]
    search_fields = ['name', ]
    ordering = ['name', ]
    fields = (
        ('credit', 'employee_initial', ),
        'name',
        'email',
        'notes',
        'orders',
        'buylist_submissions',
    )


@admin.register(StoreCredit)
class StoreCreditAdmin(admin.ModelAdmin):
    search_fields = ['name', 'date_time', ]
    list_display = ['name', 'store_credit', 'used_credit', 'date_time', 'total', ]
