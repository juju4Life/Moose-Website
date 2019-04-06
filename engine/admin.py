import os
from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse
from .models import Product, Orders, ForeignOrder, TcgCredentials, UpdatedInventory, CaseCards, StoreDatabase, MtgDatabase, MTG, Upload, Events, Yugioh, Pokemon
from simple_history.admin import SimpleHistoryAdmin
from customer.models import Preorder, Customer, PreordersReady, OrderRequest, ReleasedProducts
from django.contrib.auth.models import Group
from customer.tasks import alert
from ipware import get_client_ip
from decimal import Decimal
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from import_export import resources
from import_export.fields import Field
from import_export.forms import ConfirmImportForm
from .tcgplayer_api import TcgPlayerApi
from django.core.exceptions import PermissionDenied
from django.utils.encoding import force_text
from collections import Counter, OrderedDict, defaultdict
from tablib import Dataset

try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO

# Api calls to TCGplayer
api = TcgPlayerApi()


@admin.register(Yugioh)
class YugiohAdmin(admin.ModelAdmin):
    pass


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    pass

class UpdateResource(resources.ModelResource):

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        temp = dataset.headers
        dataset.insert(0, temp)
        dataset.headers = ['sku', 'upload_quantity']
        dataset.insert_col(0, col=["", ] * dataset.height, header="id")

    category = Field(attribute='category', column_name='category')
    name = Field(attribute='name', column_name='Name')
    group_name = Field(attribute='group_name', column_name='Set')
    foil = Field(attribute='printing', column_name='Foil')
    condition = Field(attribute='condition', column_name='Condition')
    language = Field(attribute='language', column_name='Language')
    upload_date = Field(attribute='upload_date', column_name='upload date')
    upload_status = Field(attribute='upload_status', column_name='upload status')

    class Meta:
        model = Upload
        exclude = ('upload_price',)


@admin.register(Upload)
class UploadAdmin(ImportExportModelAdmin):
    def import_action(self, request, *args, **kwargs):
        '''
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        '''
        if not self.has_import_permission(request):
            raise PermissionDenied

        resource = self.get_import_resource_class()(**self.get_import_resource_kwargs(request, *args, **kwargs))

        context = self.get_import_context_data()

        import_formats = self.get_import_formats()
        fixed_file = BytesIO()
        if request.FILES.get('import_file'):

            lines = request.FILES.get('import_file').read()
            if lines:
                formated = defaultdict(int)
                for line in lines.decode('utf-8').split("\n"):
                    line = line.strip()
                    if len(line):
                        split_line = line.split(",")
                        sku = split_line[0]
                        qty = split_line[1]
                        formated[sku] += int(qty)
                for k, v in formated.items():
                    fixed_file.write(str.encode(f"{k},{v}" + "\r\n"))
                fixed_file.seek(0, os.SEEK_END)
                size = fixed_file.tell()

                request.FILES['import_file'] = InMemoryUploadedFile(fixed_file, 'import_file', 'file.csv', 'text/csv', size, None)

        form_type = self.get_import_form()
        form = form_type(import_formats,
                         request.POST or None,
                         request.FILES or None)

        if request.POST and form.is_valid():
            input_format = import_formats[
                int(form.cleaned_data['input_format'])
            ]()
            import_file = form.cleaned_data['import_file']
            # first always write the uploaded file to disk as it may be a
            # memory file or else based on settings upload handlers
            tmp_storage = self.write_to_tmp_storage(import_file, input_format)

            # then read the file, using the proper format-specific mode
            # warning, big files may exceed memory
            try:
                data = tmp_storage.read(input_format.get_read_mode())
                if not input_format.is_binary() and self.from_encoding:
                    data = force_text(data, self.from_encoding)
                dataset = input_format.create_dataset(data)
            except UnicodeDecodeError as e:
                return HttpResponse(_(u"<h1>Imported file has a wrong encoding: %s</h1>" % e))
            except Exception as e:
                return HttpResponse(_(u"<h1>%s encountered while trying to read file: %s</h1>" % (type(e).__name__, import_file.name)))
            result = resource.import_data(dataset, dry_run=True,
                                          raise_errors=False,
                                          file_name=import_file.name,
                                          user=request.user)

            context['result'] = result

            if not result.has_errors() and not result.has_validation_errors():
                context['confirm_form'] = ConfirmImportForm(initial={
                    'import_file_name': tmp_storage.name,
                    'original_file_name': import_file.name,
                    'input_format': form.cleaned_data['input_format'],
                })

        context.update(self.admin_site.each_context(request))

        context['title'] = _("Import")
        context['form'] = form
        context['opts'] = self.model._meta
        context['fields'] = [f.column_name for f in resource.get_user_visible_fields()]

        request.current_app = self.admin_site.name
        return TemplateResponse(request, [self.import_template_name],
                                context)

    resource_class = UpdateResource
    ordering = ['upload_status', '-upload_date']
    search_fields = ['name', ]
    list_display = ['category', 'printing', 'name', 'group_name', 'condition', 'language', 'upload_price', 'upload_quantity', 'upload_date', 'upload_status',
                    'sku']

# ----------------------------------------------------------------------------------------------------------------------------


class MTGResource(resources.ModelResource):
    product_name = Field(attribute='product_name', column_name='Product Name')
    set_name = Field(attribute='set_name', column_name='Set Name')
    product_line = Field(attribute='product_line', column_name='Product Line')
    title = Field(attribute='title', column_name='Title')
    rarity = Field(attribute='rarity', column_name='Rarity')
    number = Field(attribute='number', column_name='Number')
    condition = Field(attribute='condition', column_name='Condition')
    sku = Field(attribute='sku', column_name='TCGplayer Id')

    class Meta:
        model = MTG
        exclude = ('language',)
        import_id_fields = ('sku',)


@admin.register(MTG)
class MTGAdmin(ImportExportModelAdmin):
    resource_class = MTGResource
    search_fields = ['product_name']
    list_display = ['product_name', 'set_name', 'foil', 'condition', 'language']


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

        obj.employee_initial = ''
        obj.save()

        ip, is_routable = get_client_ip(request)
        alert.apply_async(que='low_priority', args=(ip, obj.name, obj.credit, obj.id,))

    save_on_top = True
    history_list_display = ['credit', 'medal', 'employee_initial', 'changeReason', ]
    list_display = ['name', 'credit', 'notes', 'medal', 'email', ]
    search_fields = ['name']
    ordering = ['name']
    fields = (
        ('credit', 'employee_initial', ),
        'name',
        ('tournament_entry', 'tournament_results_credit',),
        'email',
        'medal',
        'notes',
    )


class PreorderAdmin(admin.ModelAdmin):
    save_on_top = True
    model = [Preorder]


class CaseCardsAdmin(admin.ModelAdmin):
    ordering = ['Update_status', 'name']
    search_fields = ['name']
    list_display = ['name', 'expansion', 'Update_status', 'price']


class PreordersReadyAdmin(SimpleHistoryAdmin):
    save_on_top = True
    history_list_display = ['name', 'price', 'paid']
    list_display = ['product', 'name', 'price', 'paid', 'quantity']
    list_filter = ['product']

    def save_model(self, request, obj, form, change):
        obj.employee_initial = ''
        obj.save()


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
    list_filter = ['foil', 'language', 'condition', 'expansion']
    readonly_fields = ('sku', 'product_id', 'condition', 'name', 'expansion', 'image', 'foil', 'language')
    fieldsets = (
        (None, {
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
admin.site.register(MtgDatabase)
admin.site.register(OrderRequest, OrderRequestAdmin)
admin.site.unregister(Group)
