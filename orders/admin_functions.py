from django.utils.html import format_html


def show_firm_url(obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.order_view)






