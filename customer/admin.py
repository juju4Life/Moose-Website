from django.contrib import admin
from .models import ItemizedPreorder, Customer
from simple_history.admin import SimpleHistoryAdmin


# Register your models here.


@admin.register(ItemizedPreorder)
class ItemPreorderAdmin(admin.ModelAdmin):
    list_display = ['name', 'expansion', 'price', 'quantity', 'available', 'total_sold']
    ordering = ['price']


@admin.register(Customer)
class CustomerAdmin(SimpleHistoryAdmin):

    # ip, is_routable = get_client_ip(request)

    # alert.apply_async(que='low_priority', args=(ip, obj.name, obj.credit, obj.id,))

    save_on_top = True
    history_list_display = ['credit', 'employee_initial', 'changeReason', ]
    list_display = ['name', 'credit', 'email', 'notes', ]
    search_fields = ['name']
    ordering = ['name', ]
    fields = (
        ('credit', 'employee_initial',),
        ('name', 'email', ),
        'notes',
    )


