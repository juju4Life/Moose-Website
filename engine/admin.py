from django.contrib import admin
from .models import Product, Orders, ForeignOrder, TcgCredentials, UpdatedInventory, CaseCards, StoreDatabase
from simple_history.admin import SimpleHistoryAdmin
from customer.models import Preorder, Customer, PreordersReady, OrderRequest, ReleasedProducts
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from customer.tasks import alert
from ipware import get_client_ip
from decimal import Decimal
from simple_history.utils import update_change_reason


class MasterAdmin(admin.ModelAdmin):
    model = Product
   # ordering = ['name']
    list_display = ('name', 'set_name')
    search_fields = ['name']
    list_filter = ['site']



class OrdersProcessingAdmin(admin.ModelAdmin):
    model = Orders
    #full_order()
    fieldsets = (
        (None,{
            'fields': (
                ('shipping_name', 'order_number',),
                ('order_date', 'order_status_type',),
                'order_details',
                ('order_delivery_type', 'shipping_address'),
            )
        }),

        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('net_profit', 'token', 'name'),
        }),
    )

    ordering = ['order_date']
    list_display = ( 'order_date', 'shipping_name', 'order_number', 'order_status_type',)
    search_fields = ['order_details']
    list_filter = ('order_status_type',)
    actions = ['order']


class ForeignAdmin(admin.ModelAdmin):
    model = ForeignOrder
    ordering = ['-order_date']
    search_fields = ['cards']
    list_display = ('cards', 'order_date')
    fields = (('order_number', 'order_date'), 'cards',)


class UpdatedInventoryAdmin(admin.ModelAdmin):
    ordering = ['-change_date', 'expansion', 'name']
    search_fields = ['name']
    list_display = ('name', 'expansion','condition', 'updated_price', 'previous_price', 'direct_price', 'market_price', 'low_price', 'mid_price', 'change_date',)
    list_filter = ('change_date' ,'expansion')


class CustomerAdmin(SimpleHistoryAdmin):
    def save_model(self, request, obj, form, change):
        if obj.tournament_entry == 'mtg locals':
            obj.credit -= Decimal(10)
            obj.tournament_entry = 'none'
            obj.history_change_reason = 'mtg weekly event entry'
            obj.save()

        elif obj.tournament_entry == 'yugioh locals':
            obj.credit -= Decimal(5)
            obj.tournament_entry = 'none'
            obj.history_change_reason = 'yugioh local entry'
            obj.save()

        if obj.tournament_results_credit != 'none':
            obj.credit += Decimal(obj.tournament_results_credit)
            obj.tournament_results_credit = 'none'
            obj.history_change_reason = "{} add for tournament".format(obj.tournament_results_credit)
            obj.save()

        if obj.tournament_results_credit == 'none' and obj.tournament_entry == 'none':
            obj.save()


        ip, is_routable = get_client_ip(request)
        alert.apply_async(que='low_priority', args=(ip, obj.name, obj.credit, obj.id,))


    save_on_top = True
    history_list_display = ['credit', 'medal', 'changeReason']
    list_display = ['name', 'credit','notes', 'medal', 'email',]
    search_fields = ['name']
    ordering = ['name']
    fields = (
        'credit',
        'name',
        ('tournament_entry', 'tournament_results_credit',),
        'email',
        'medal',
        'notes',
    )




class PreorderAdmin(admin.ModelAdmin):
    save_on_top = True
    model = [Preorder]
    search_fields = ['name']



class CaseCardsAdmin(admin.ModelAdmin):
    ordering = ['Update_status' ,'name']
    search_fields = ['name']
    list_display = ['name', 'expansion', 'Update_status', 'price']



class PreordersReadyAdmin(SimpleHistoryAdmin):
    save_on_top = True
    history_list_display = ['name', 'price', 'paid']
    list_display = ['product','name' ,'price', 'paid', 'quantity']
    search_fields = ['name']
    list_filter = ['product']
    autocomplete_fields = ['customer_name', 'product']


class OrderRequestAdmin(admin.ModelAdmin):
    ordering = ['-date']
    list_display = ['name', 'date', 'total']
    fields = (
        'date',
        ('name', 'contact_type',),
        ('email', 'phone',),
        ('missing', 'total',),
        'notes',
        'order_link',
        'order',
    )


class ReleasedProductsAdmin(admin.ModelAdmin):
    ordering = ['release_date']
    list_display = ['product', 'release_date', 'price', 'link']


class StoreDatabaseAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'expansion', 'condition', 'language', 'foil']
    list_filter = ['foil', 'language', 'condition']
    readonly_fields = ('sku', 'product_id', 'condition', 'name', 'expansion', 'image', 'foil', 'language')
    fieldsets = (
        (None,{
            'fields': (
                'foil',
                ('quantity', 'condition',),
                'custom_percentage',
                'name',
                'expansion',
                'language',
            )
        }),

        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('sku', 'product_id', 'image'),
        }),
    )





admin.site.site_header = 'MTGFIRST ADMIN'
admin.site.site_title = ''
admin.site.index_title = ''
admin.site.index_title = ''
admin.site.register(UpdatedInventory, UpdatedInventoryAdmin)
admin.site.register(CaseCards, CaseCardsAdmin)
admin.site.register(StoreDatabase, StoreDatabaseAdmin)
admin.site.register(PreordersReady, PreordersReadyAdmin)
admin.site.register(Preorder, PreorderAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Orders, OrdersProcessingAdmin)
admin.site.register(Product, MasterAdmin)
admin.site.register(ReleasedProducts, ReleasedProductsAdmin)
admin.site.register(ForeignOrder, ForeignAdmin)
admin.site.register(TcgCredentials)
admin.site.register(OrderRequest, OrderRequestAdmin)
admin.site.unregister(Group)
