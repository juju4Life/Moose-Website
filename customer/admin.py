from django.contrib import admin
from customer.models import Customer, StoreCredit
from customer.stats import Stats
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
        ('credit', 'clear_credit', ),
        ('transaction', 'employee_initial', ),
        'name',
        'email',
        'notes',
        'orders',
        'buylist_submissions',
    )


@admin.register(StoreCredit)
class StoreCreditAdmin(admin.ModelAdmin):
    search_fields = ['name', 'date_time', ]
    list_display = ['name', 'store_credit', 'used_credit', 'date_time', 'transaction_type', 'total', ]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['n_day_in_out_graph'] = Stats().store_credit_daily_transactions()['in_out_graph']
        extra_context['n_day_volume_graph'] = Stats().store_credit_daily_transactions()['ninety_day_volume']
        extra_context['ytd_by_month_credit_added'] = Stats().store_credit_by_month()['ytd_credit_added_by_month']
        extra_context['ytd_by_month_credit_spent'] = Stats().store_credit_by_month()['ytd_credit_spent_by_month']
        return super(StoreCreditAdmin, self).changelist_view(
            request, extra_context=extra_context,
        )

