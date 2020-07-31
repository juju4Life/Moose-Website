import string
import tablib
from time import localtime, strftime

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.models import Group
from django.db.models import Q
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from engine.models import MTG, DirectData, TcgGroupPrice, MooseInventory, MooseAutopriceMetrics, CardPriceData, MtgCardInfo
from engine.tcgplayer_api import TcgPlayerApi

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field

api = TcgPlayerApi('first')


@admin.register(MtgCardInfo)
class MTGCardInfo(admin.ModelAdmin):
    pass

# TcgPlayer Buylist Hub --------------------------------------------------------------------------------------------------------------------


class CardDataResource(resources.ModelResource):
    name = Field(attribute='name', column_name='Name')
    expansion = Field(attribute='expansion', column_name='Set')
    tcg_net = Field(attribute='tcg_net', column_name='Tcg Net')
    tcg_price = Field(attribute='tcg_price', column_name='Tcg Price')
    tcg_market = Field(attribute='tcg_market', column_name='Tcg Market')
    amazon_price = Field(attribute='amazon_price', column_name='Amazon Price')
    amazon_net = Field(attribute='amazon_net', column_name='Amazon Net')
    scg_buylist = Field(attribute='scg_buylist', column_name='SCG Buylist')
    ck_buylist = Field(attribute='ck_buylist', column_name='CK Buylist')

    class Meta:
        model = CardPriceData
        exclude = ('id', 'cfb_buylist', 'direct_net', 'store_quantity_needed', 'printing', 'sell_to', 'best_net',
                   'sku', 'product_id', 'tcg_direct_price', 'updated',)


@admin.register(CardPriceData)
class CardPriceAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'expansion', 'ck_buylist', 'scg_buylist', 'tcg_direct_price', 'tcg_price', 'amazon_price', 'low_store_stock',
                    'store_quantity_needed', 'sell_to', 'updated', ]
    ordering = ['name']
    resource_class = CardDataResource


# TcgPlayer Buylist Hub END --------------------------------------------------------------------------------------------------------------------


# Moose Tcg Auto Price Metrics ----------------- START
@admin.register(MooseAutopriceMetrics)
class MooseMetricsAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['old_price', 'updated_price', 'name', 'expansion', 'condition', 'printing', 'updated_at',
                    'price_1', 'price_1_gold',
                    'price_2', 'price_2_gold',
                    'price_3', 'price_3_gold',
                    'price_4', 'price_4_gold',
                    'price_5', 'price_5_gold', ]


# Moose Tcg Auto Pricer Metrics ----------------- END


@admin.register(MooseInventory)
class MooseInv(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'expansion', 'condition', 'updated_price']


# Magic the Gathering Card Database ------------------ START

class AlphabetFilter(SimpleListFilter):
    title = "Staring Character"
    parameter_name = ""

    def lookups(self, request, model_admin):
        characters = string.ascii_uppercase

        characters = ((i, i,) for i in characters)
        return list(characters)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Q(name__startswith=self.value()))


class MTGResource(resources.ModelResource):

    product_id = Field(attribute='product_id', column_name='Id')
    name = Field(attribute='name', column_name='Name')
    expansion = Field(attribute='expansion', column_name='Set')
    normal_clean_stock = Field(attribute='normal_clean_stock', column_name='Normal Clean')
    normal_played_stock = Field(attribute='normal_played_stock', column_name='Normal Played')
    normal_heavily_played_stock = Field(attribute='normal_heavily_played_stock', column_name='Normal Heavy')
    foil_clean_stock = Field(attribute='foil_clean_stock', column_name='Foil Clean')
    foil_played_stock = Field(attribute='foil_played_stock', column_name='Foil Played')
    foil_heavily_played_stock = Field(attribute='foil_heavily_played_stock', column_name='Foil Heavy')

    class Meta:
        model = MTG
        fields = ('product_id', 'name', 'expansion', 'normal_clean_stock', 'normal_played_stock', 'normal_heavily_played_stock',
                  'foil_clean_stock', 'foil_played_stock', 'foil_heavily_played_stock',)
        exclude = ('language',)
        import_id_fields = ('product_id',)


@admin.register(MTG)
class MTGAdmin(ImportExportModelAdmin):

    def import_action(self, request, *args, **kwargs):
        """
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        """
        if not self.has_import_permission(request):
            raise PermissionDenied

        context = self.get_import_context_data()

        import_formats = self.get_import_formats()
        form_type = self.get_import_form()
        form_kwargs = self.get_form_kwargs(form_type, *args, **kwargs)
        form = form_type(import_formats,
                         request.POST or None,
                         request.FILES or None,
                         **form_kwargs)

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
                # Id,Name,Set,Normal Clean,Normal Played,Normal Heavy,Foil Clean,Foil Played,Foil Heavy

                # filter the data
                data_new = data.split('\n')
                headers = data_new[0]
                rows = data_new[1:]
                new_rows = []
                try:
                    for row in rows:
                        row = row.split(',')
                        if int(row[3]) > 0 or int(row[4]) > 0 or int(row[5]) > 0:
                            new_rows.append(','.join(row))
                except ValueError:
                    pass
                new_rows = [headers] + new_rows
                data = '\n'.join(new_rows)

                if not input_format.is_binary() and self.from_encoding:
                    data = force_str(data, self.from_encoding)
                dataset = input_format.create_dataset(data)
            except UnicodeDecodeError as e:
                return HttpResponse(_(u"<h1>Imported file has a wrong encoding: %s</h1>" % e))
            except Exception as e:
                return HttpResponse(_(u"<h1>%s encountered while trying to read file: %s</h1>" % (type(e).__name__, import_file.name)))

            # prepare kwargs for import data, if needed
            res_kwargs = self.get_import_resource_kwargs(request, form=form, *args, **kwargs)
            resource = self.get_import_resource_class()(**res_kwargs)

            # prepare additional kwargs for import_data, if needed
            imp_kwargs = self.get_import_data_kwargs(request, form=form, *args, **kwargs)
            result = resource.import_data(dataset, dry_run=True,
                                          raise_errors=False,
                                          file_name=import_file.name,
                                          user=request.user,
                                          **imp_kwargs)

            context['result'] = result

            if not result.has_errors() and not result.has_validation_errors():
                initial = {
                    'import_file_name': tmp_storage.name,
                    'original_file_name': import_file.name,
                    'input_format': form.cleaned_data['input_format'],
                }
                confirm_form = self.get_confirm_import_form()
                initial = self.get_form_kwargs(form=form, **initial)
                context['confirm_form'] = confirm_form(initial=initial)
        else:
            res_kwargs = self.get_import_resource_kwargs(request, form=form, *args, **kwargs)
            resource = self.get_import_resource_class()(**res_kwargs)

        context.update(self.admin_site.each_context(request))

        context['title'] = _("Import")
        context['form'] = form
        context['opts'] = self.model._meta
        context['fields'] = [f.column_name for f in resource.get_user_visible_fields()]

        request.current_app = self.admin_site.name
        return TemplateResponse(request, [self.import_template_name],
                                context)

    def get_export_filename(self, request, queryset, file_format):
        date_time = strftime("%Y-%m-%d %I_%M%p", localtime())
        filename = f"{queryset[0].name[0]} - {date_time}.csv"

        return filename

    resource_class = MTGResource
    search_fields = ['name']
    list_display = ['name', 'expansion', 'language', ]
    list_filter = [AlphabetFilter, ]
    ordering = ["name", "expansion", ]



# Magic the Gathering Card Database ------------------ END


@admin.register(TcgGroupPrice)
class TcgGroupPriceAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    list_display = ['name', 'expansion', 'direct_low_price', 'market_price', 'low_price', 'mid_price', 'printing', ]


@admin.register(DirectData)
class DirectTrackerAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'expansion', 'consecutive_days_non_direct', 'total_days_non_direct', 'condition', 'foil', 'last_add', 'in_stock',
                    'current_price', 'low', 'market', ]
    ordering = ['-in_stock', '-last_add', '-consecutive_days_non_direct', ]


admin.site.site_header = 'MooseLoot'
admin.site.site_title = ''
admin.site.index_title = 'MooseLoot'
admin.site.unregister(Group)
