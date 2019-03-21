import requests
import base64
from urllib.parse import unquote
from decouple import config
from .models import EbayAccessToken


class EbayApi:
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

        url = ''
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

    def create_item(self, sku, title, expansion, image_url, quantity, condition='Near Mint / Lightly Played'):
        url = self.base_url + f'inventory_item/{sku}'
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Language': 'en-US',
        }

        data = {
            "availability": {
                "shipToLocationAvailability": {
                    "quantity": quantity,
                }
            },
            "condition": "NEW",
            "product": {
                "title": title,
                "description": f"<strong>Shipping for this item is Fast and Free</strong>\n\n"
                f"This auction is for <strong>{quantity}x {title}</strong> from the {expansion} expansion and will be in"
                f"<strong>{condition}</strong> condition.\n\nThese card(s) will be  inserted into a sleeve, top-loader, team  bag, and padded bubble-mailer "
                f"envelop to provide the maximum level of protection for your purchase.\n\nWe have many great auctions at affordable prices, "
                f"and provide combined shipping. Check our our extensive inventory of Magic the Gathering Singles\n\n"
                f"We pride ourselves in our  first-class service. If there is anything  we can do to provide a better experience,  don't hesitate"
                " to contact us.\n",

                "aspects": {
                    "Brand": [
                        "Magic the Gathering"
                    ],
                    "Type": [
                        "Trading card"
                    ],

                },
                "brand": "Wizards of the Coast",
                "mpn": "WOtC",
                "imageUrls": [
                    image_url,
                ]
            }
        }

        r = requests.put(url, headers=headers, json=data)
        print(r)

    def create_offer(self, sku, quantity, category_id):
        url = self.base_url + 'offer'
        headers = self.return_headers('Bearer', content_language=True)
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
            'code': unquote(self.credentials.user_token),
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
        self.credentials.access_token = token_data['access_token']
        self.credentials.save()





