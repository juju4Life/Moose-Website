from buylist.models import SkuLight
from engine.tcgplayer import create_tcg_buylist, TcgPlayerApi
from.models import ReleasedProducts
from datetime import date
from .fix_words import FixWords

fix = FixWords()

class GetCards:
    sku_light = SkuLight.objects
    tcg = TcgPlayerApi()
    def buylist_by_name(self, card_name):
        sku = self.sku_light.filter(name=card_name)
        if not sku.exists():
            return 'error'
        else:
            m = []
            for card in sku:
                msg = ("{}\n({})\n${}\n\n".format(card.name, card.expansion, create_tcg_buylist(card.sku)))
                m.append(msg)
            m = ','.join(m)
            results = "TcgPlayer Buylist Updated\n\n" + m
            return results


    def buylist_by_name_and_set(self, card_set, card_name):
        sku = self.sku_light.filter(expansion=card_set).filter(name=card_name)
        if not sku.exists():
            return 'error'
        else:
            m = []
            for card in sku:
                msg = ("{}\n({})\n${}\n\n".format(card.name, card.expansion, create_tcg_buylist(card.sku)))
                m.append(msg)
            m = ','.join(m)
            results = "TcgPlayer Buylist Updated\n\n" + m
            return results

    def search_by_name_and_set(self, card_name, card_set):
        sku = self.sku_light.filter(expansion=card_set).filter(name=card_name)
        if not sku.exists():
            return 'error'
        else:
            m = []
            for card in sku:
                inventory = self.tcg.search_inventory(self.tcg.card_info_by_sku(card.sku)['results'][0]['productId'])['results'][0][
                    'totalQuantity']
                msg = ("{}\n({})\nQuantity: {}\n\n".format(card.name, card.expansion, inventory))
                m.append(msg)
            m = ','.join(m)
            results = "Online Inventory: \n\n" + m
            return results


    def search_by_name(self, card_name):
        sku = self.sku_light.filter(name=card_name)
        if not sku.exists():
            return 'error'
        else:
            m = []
            for card in sku:
                inventory = self.tcg.search_inventory(self.tcg.card_info_by_sku(card.sku)['results'][0]['productId'])['results'][0][
                    'totalQuantity']
                msg = ("{}\n({})\nQuantity: {}\n\n".format(card.name, card.expansion, inventory))
                m.append(msg)
            m = ','.join(m)
            results = "Online Inventory: \n\n" + m
            return results



class GetProducts:
    products = ReleasedProducts.objects
    month_dictionary = {
        'jan': 'january',
        'feb': 'february',
        'mar': 'march',
        'apr': 'april',
        'may': 'may',
        'jun': 'june',
        'jul': 'july',
        'aug': 'august',
        'sep': 'september',
        'oct': 'october',
        'nov': 'november',
        'dec': 'december',
        'january': 'january',
        'february': 'february',
        'march': 'march',
        'april': 'april',
        'june': 'june',
        'july': 'july',
        'august': 'august',
        'september': 'september',
        'october': 'october',
        'november': 'november',
        'december': 'december',

    }


    def by_month(self, month, year=date.today().year):
        try:
            _month = self.month_dictionary[month]
            products_by_month = self.products.filter(month=self.month_dictionary[_month]).filter(year=year)

            if not products_by_month.exists():
                print("THIS", _month)
                if fix.month_to_integer(_month) < date.today().month:
                    if int(year) <= date.today().year + 1 and int(year) > 1993:
                        results_list = []
                        last_year_results = self.products.filter(month=self.month_dictionary[_month]).filter(
                            year=(str(int(year) - 1)))
                        for each in last_year_results:
                            results = "{}\n" \
                                      "MSRP: {}\n" \
                                      "Released: {}\n\n".format(each.product, each.price, each.release_date)
                            results_list.append(results)
                        results_list = ','.join(results_list)
                        return "Last Year's Products:\n\n{}".format(results_list)
                    else:
                        return "No Products in database for that year"

                else:
                    return "No Results for products in {}/{}".format(_month, year)

            else:
                results_list = []
                for each in products_by_month:
                    results = "{}\n" \
                              "MSRP: {}\n" \
                              "Released: {}\n\n".format(each.product, each.price, each.release_date)
                    results_list.append(results)
                results_list = ','.join(results_list)
                return "Products\n\n{}".format(results_list)

        except KeyError:
            return 'Incorrect format/spelling for month. Must be like "jan" or "january" '

    def upcoming(self):
        products = self.products.all()
        results_list = []
        for each in products:
            if fix.month_to_integer(each.month.lower()) >= date.today().month and fix.month_to_integer(each.month.lower()) < date.today().month + 2:
                results_list.append(
                    "{}\n" \
                    "MSRP: {}\n" \
                    "Released: {}\n\n".format(each.product, each.price, each.release_date)
                )

        results_list = ','.join(results_list)
        return "Upcoming Products\n\n{}".format(results_list)








