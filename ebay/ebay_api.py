import requests
import base64
from urllib.parse import unquote
from decouple import config
from .models import EbayAccessToken


class EbayCredentials:
    credentials = EbayAccessToken.objects.get(name='')
    base_url = 'https://api.ebay.com/sell/inventory/v1/'
    access_token = credentials.access_token
    refresh_token = credentials.refresh_token
    client_id = config('ebay_client_id')
    client_secret = config('ebay_client_secret')

    refresh_token = 'v^1.1#i^1#p^3#f^0#r^1#I^3#t^Ul4xMF81OjcwNDYwRTZGODczQzE4QzI4MDhFRTRFMUU4QTkyQkU1XzNfMSNFXjI2MA=='
    encoded_credentials = base64.b64encode(b'%s' % f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')
    user_request_id = credentials.user_token
    scopes = [
        'https://api.ebay.com/oauth/api_scope ',
        'https://api.ebay.com/oauth/api_scope/sell.marketing.readonly ',
        'https://api.ebay.com/oauth/api_scope/sell.marketing ',
        'https://api.ebay.com/oauth/api_scope/sell.inventory.readonly ',
        'https://api.ebay.com/oauth/api_scope/sell.inventory ',
        'https://api.ebay.com/oauth/api_scope/sell.account.readonly ',
        'https://api.ebay.com/oauth/api_scope/sell.account ',
        'https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly ',
        'https://api.ebay.com/oauth/api_scope/sell.fulfillment ',
        'https://api.ebay.com/oauth/api_scope/sell.analytics.readonly',
    ]

    encoded_scopes = ''.join(scopes)

    def return_headers(self, auth_type, content_type='application/json', content_language=False, accept=False):
        if auth_type == 'Bearer':
            if accept is True:
                if content_language is True:
                    headers = {
                        'Authorization': 'Bearer ' + self.access_token,
                        'Content-Language': 'en-US',
                        'Accept': 'application/json',
                        'Content-Type': content_type,
                    }
                else:
                    headers = {
                        'Content-Type': content_type,
                        'Accept': 'application/json',
                        'Authorization': 'Bearer ' + self.access_token
                    }
            else:
                if content_language is True:
                    headers = {
                        'Content-Type': content_type,
                        'Content-Language': 'en-US',
                        'Authorization': 'Bearer ' + self.access_token
                    }
                else:
                    headers = {
                        'Content-Type': content_type,
                        'Authorization': 'Bearer ' + self.access_token
                    }
        else:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'{auth_type} {self.encoded_credentials}'
            }
        return headers

    def migrate_obj(self):
        headers = self.return_headers('Bearer', accept=True)

        url = self.call_url
        data = {
              "requests": [
                {
                  "listingId": "163447808844"
                }
              ]
            }
        r = requests.post(url, headers=headers, json=data)
        return r.json()

    def get_inventory(self):
        path = f'https://api.ebay.com/sell/inventory/v1/inventory_item'

        headers = self.return_headers('Bearer')

        params = {
            'limit': 100,
            'offset': 0,
        }

        r = requests.get(path, headers=headers, params=params)
        return r.json()

    def get_item(self, sku):
        path = f'https://api.ebay.com/sell/inventory/v1/inventory_item/{sku}'

        headers = self.return_headers('Bearer')

        r = requests.get(path, headers=headers)
        return r.json()

    def create_item(self, sku):
        url = self.base_url + f'inventory_item/{sku}'
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Language': 'en-US',
        }

        data = {
            "availability": {
                "shipToLocationAvailability": {
                    "quantity": 10
                }
            },
            "condition": "NEW",
            "product": {
                "title": "Snapcaster Mage",
                "description": "SNap Card from the Innistrad expansion set",
                "aspects": {
                    "Brand": [
                        "Magic the Gathering"
                    ],
                    "Type": [
                        "Trading Card"
                    ],

                },
                "brand": "Wizards of the Coast",
                "mpn": "WOC",
                "imageUrls": [
                    "https://img.scryfall.com/cards/large/front/7/e/7e41765e-43fe-461d-baeb-ee30d13d2d93.jpg?1547516526",
                ]
            }
        }

        r = requests.put(url, headers=headers, json=data)
        print(r)

    def create_offer(self, sku, quantity, category_id):
        url = self.base_url + 'offer'
        headers = self.return_headers('Bearer', content_language=True)
        print(headers)
        data = {
            "sku": sku,
            "marketplaceId": "EBAY_US",
            "merchantLocationKey": "US_21060",
            "format": "FIXED_PRICE",
            "availableQuantity": quantity,
            "categoryId": category_id,
            "listingDescription": "1x Arid Mesa from the Zendikar expansion set.",
            "listingPolicies": {
                "fulfillmentPolicyId": "33310623022",
                "paymentPolicyId": "24992594022",
                "returnPolicyId": "153557924022"
            },
            "pricingSummary": {
                "price": {
                    "currency": "USD",
                    "value": "59.99"
                }
            },

            "quantityLimitPerBuyer": 4
        }

        r = requests.post(url, headers=headers, json=data)
        return r.json()

    def get_policies(self, policy):
        url = f'https://api.ebay.com/sell/account/v1/{policy}'
        params = {
            'marketplace_id': 'EBAY_US'
        }
        headers = self.return_headers('Bearer')
        r = requests.get(url, headers=headers, params=params)
        return r.json()

    def create_fulfillment_policy(self):
        url = 'https://api.ebay.com/sell/account/v1/fulfillment_policy'
        print(url)

        data = {
            "categoryTypes": [
                {
                    "name": "ALL_EXCLUDING_MOTORS_VEHICLES"
                }
            ],
            "marketplaceId": "EBAY_US",
            "name": "Domestic free shipping",
            "handlingTime": {
                "unit": "DAY",
                "value": "1"
            },
            "shippingOptions": [
                {
                    "costType": "FLAT_RATE",
                    "optionType": "DOMESTIC",
                    "shippingServices": [
                        {
                            "buyerResponsibleForShipping": "false",
                            "freeShipping": "true",
                            "shippingCarrierCode": "USPS",
                            "shippingServiceCode": "USPSPriorityFlatRateBox"
                        }
                    ]
                }
            ]
        }
        headers = self.return_headers('Bearer')
        r = requests.post(url, headers=headers, data=data)
        return r.json()

    def publish_offer(self, offer_id):
        url = self.base_url + f'offer/{offer_id}/publish'
        headers = self.return_headers('Bearer')
        r = requests.post(url, headers=headers)
        return r.json()

    def get_locations(self):
        url = self.base_url + 'location'
        headers = self.return_headers('Bearer')
        r = requests.get(url, headers=headers)
        return r.json()

    def get_oath_token(self):
        url = 'https://api.ebay.com/identity/v1/oauth2/token'
        headers = self.return_headers('Basic')
        data = {
            'grant_type': 'authorization_code',
            'code': unquote(self.client_id),
            'redirect_uri': 'Jermol_Jupiter-JermolJu-Search-nnlcpv',
            'scope': self.encoded_scopes,
        }
        r = requests.post(url, headers=headers, data=data)
        token_data = r.json()
        access_token = token_data['access_token']
        expires = token_data['expires_in']
        refresh_token = token_data['refresh_token']
        refresh_token_expiration = token_data['refresh_token_expires_in']
        return {
            'access_token': access_token,
            'token_expiration': expires,
            'refresh_token': refresh_token,
            'refresh_expiration': refresh_token_expiration,
        }

    def refresh(self):
        headers = self.return_headers('Basic')
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'scope': self.encoded_scopes,
        }
        url = 'https://api.ebay.com/identity/v1/oauth2/token'
        r = requests.post(url, headers=headers, data=data)
        token_data = r.json()
        print(token_data)
        with open('token.txt', 'w') as f:
            f.write(token_data['access_token'])
        return token_data


# call = EbayCredentials().create_offer('mtg-3459022', quantity='3', category_id='38292')

# print(EbayCredentials().publish_offer('46220752019'))
# print(EbayCredentials().get_locations())

ebay = EbayCredentials()


def list_item(sku):
    ebay.create_item(sku)
    offer_id = ebay.create_offer(sku, quantity=5, category_id='38292')['offerId']
    print(ebay.publish_offer(offer_id))


print(ebay.get_inventory())

