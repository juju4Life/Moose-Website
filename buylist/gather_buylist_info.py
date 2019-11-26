from buylist.models import StarcityBuylist, CardKingdomBuylist
from engine.models import CardPriceData
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def add_buylist_data():
    card_data = CardPriceData.objects.all()

    for index, card in enumerate(card_data):

        try:
            scg_card = StarcityBuylist.objects.exclude(is_foil=True).filter(expansion=card.expansion).get(name=card.name)
            card.scg_buylist = scg_card.price_nm
        except MultipleObjectsReturned as e:
            print(e)
        except ObjectDoesNotExist:
            pass

        try:
            ck_card = CardKingdomBuylist.objects.exclude(is_foil=True).filter(expansion=card.expansion).get(name=card.name)
            card.ck_buylist = ck_card.price_nm
        except MultipleObjectsReturned as e:
            print(e)
        except ObjectDoesNotExist:
            pass

        card.save()















