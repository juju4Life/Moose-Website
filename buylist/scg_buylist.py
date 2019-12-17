from time import sleep
import requests
from my_customs.standardize_sets import Standardize
from my_customs.decorators import report_error
from buylist.models import StarcityBuylist
from other.gather_analytics import analyze
from other.models import StarCityAnalytics

standardize = Standardize()

id_list = [
        '5061', '5275', '1003', '1009', '5276', '1015', '1025', '1037', '1053', '5023', '5344', '5131', '1012', '1000', '5355', '1068', '1005', '1039', '1004',
        '5190', '5191', '5365', '5359', '5228', '5308', '1069', '5382', '1070', '1001', '5018', '5271', '5005', '1062', '5040', '5057', '5009', '5213', '5269',
        '5294', '5313', '5346', '5364', '5391', '5413', '5358', '5386', '5338', '5247', '5116', '5286', '5334', '5384', '5409', '5221', '1057', '1071', '5037',
        '5379', '5254', '5302', '5217', '5298', '5327', '5134', '5301', '5195', '5082', '5381', '5176', '5265', '5245', '5115', '5280', '5209', '5368', '5354',
        '5341', '5189', '5253', '5290', '5225', '5311', '5196', '5336', '5331', '5096', '1019', '5371', '1008', '5296', '5007', '5310', '5293', '5108', '5171',
        '5219', '5342', '5246', '5194', '5374', '5268', '5055', '5398', '5249', '5387', '5396', '5035', '5392', '1011', '5360', '1010', '5369', '5215', '5010',
        '1033', '5366', '5281', '1045', '5339', '5291', '1006', '1049', '5064', '5137', '5192', '5211', '5241', '5260', '5288', '5306', '5357', '5343', '5312',
        '5377', '1027', '1013', '1055', '5202', '5285', '5407', '5258', '5304', '5352', '5083', '5399', '1029', '5207', '5315', '1041', '1047', '5049', '5174',
        '5236', '5350', '5351', '5175', '5237', '1035', '1059', '1060', '1061', '5201', '5220', '5186', '1078', '1079', '1073', '5333', '1031', '5400', '5026',
        '5273', '5243', '5187', '5375', '5020', '5197', '1051', '5094', '5329', '5106', '5411', '5388', '1063', '1018', '1017', '1007', '5266', '5418', '5414',
        '5416', '5042', '1043', '5403', '5402', '1064', '5016', '1002', '5372', '1023', '1021', '1020', '1074', '1014', '5405', '1016', '5362', '5363', '5328',
        '5177', '5172'
    ]


def buylist_data(cat_id):

    url = f'http://old.starcitygames.com/buylist/search?search-type=category&id={cat_id}'
    results = requests.get(url).json()

    expansion = standardize.expansion(results['search'])

    data_list = []

    for card_list in results['results']:
        foil = card_list[0]['foil']
        if foil is True:
            foil = 'Foil'
        elif foil is False:
            foil = 'Normal'
        else:
            foil = ''

        name = card_list[0]['name']
        nm_price = 0
        played_price = 0
        hp_price = 0

        for card in card_list:
            if card['language'] == 'English':
                if card['condition'] == 'NM/M':
                    nm_price = card['price']
                elif card['condition'] == 'PL':
                    played_price = card['price']
                elif card['condition'] == 'HP':
                    hp_price = card['price']

        data_list.append(
            StarcityBuylist(
                name=name,
                expansion=expansion,
                printing=foil,
                price_nm=nm_price,
                price_played=played_price,
                price_hp=hp_price,
            )
        )
        analyze(
            store=StarCityAnalytics,
            name=name,
            expansion=expansion,
            printing=foil,
            buylist_price=nm_price,
        )
    return data_list


@report_error
def get_scg_buylist():
    StarcityBuylist.objects.all().delete()
    count = 0
    while count < len(id_list):
        sleep(1)
        data = buylist_data(id_list[count])
        StarcityBuylist.objects.bulk_create(data)
        print("{} sets complete".format(count+1))
        count += 1

