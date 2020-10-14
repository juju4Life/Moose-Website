from django.db import transaction
from django.db.models import Q
from engine.models import MTG


def handle_query(query, filtering, page, cards_per_page=10, check_stock=False):
    with transaction.atomic():
        if page == 'sick_deals':
            results = MTG.objects.filter(sick_deals=True).order_by(filtering)
        else:
            results = list()
            error = ''

    if check_stock:
        results = results.filter(
            Q(normal_clean_stock__gte=1) | Q(normal_played_stock__gte=1) | Q(normal_heavily_played_stock__gte=1) |
            Q(foil_clean_stock__gte=1) | Q(foil_played_stock__gte=1) | Q(foil_heavily_played_stock__gte=1)
        )

    return results, error, cards_per_page, query


def process_filter(request, page):
    if request.GET.get('all'):
        results, error, cards_per_page, query = handle_query("all", "name", page=page)

    elif request.GET.get('in_stock'):
        results, error, cards_per_page, query = handle_query("in_stock", "name", check_stock=True, page=page)

    elif request.GET.get('sort_by_set_reverse'):
        results, error, cards_per_page, query = handle_query("sort_by_set_reverse", "-expansion", page=page)

    elif request.GET.get('sort_by_set'):
        results, error, cards_per_page, query = handle_query("sort_by_set_reverse", "expansion", page=page)

    elif request.GET.get('per_page_10'):
        results, error, cards_per_page, query = handle_query("per_page_10", "name", page=page)

    elif request.GET.get('per_page_20'):
        results, error, cards_per_page, query = handle_query("per_page_20", "name", cards_per_page=20, page=page)

    elif request.GET.get('per_page_50'):
        results, error, cards_per_page, query = handle_query("per_page_50", "name", cards_per_page=50, page=page)

    elif request.GET.get('preorder'):
        query = request.GET.get('preorder')
        cards_per_page = 10
        error = ''
        results = MTG.objects.filter(expansion=query)
    else:
        return

    return results, error, cards_per_page


