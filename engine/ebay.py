import requests
import base64

USER_AUTH_TOKEN = 'v^1.1#i^1#I^3#f^0#p^3#r^0#t^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'

#base64.b64encode(b'Basic JermolJu-Searchez-SBX-cd2df7e74-7f76196a:SBX-d2df7e7437a7-596d-43a4-9563-b9b6')

def permission():
    url = 'https://auth.sandbox.ebay.com/oauth2/authorize?client_id=JermolJu-Searchez-SBX-cd2df7e74-7f76196a&redirect_uri=Jermol_Jupiter-JermolJu-Search-vrnsvq&response_type=code&scope=https://api.ebay.com/oauth/api_scope/sell.account%20https://api.ebay.com/oauth/api_scope/sell.inventory&prompt=login'



def test():
    headers = {
        'Authorization': 'Bearer ' + USER_AUTH_TOKEN,
        'Accept': 'application/json',
        'grant_type': 'authorization_code',
        'Content-Type': 'application/json'
    }

    url = 'https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search?q=drone&limit=3'

    r = requests.get(url, headers=headers)
    print(r.content)


def create_item():
    url = 'https://api.sandbox.ebay.com/sell/inventory/v1/inventory_item/GP-Cam-01'
    headers = {
        'Authorization': 'Bearer ' + USER_AUTH_TOKEN,
        'Content-Type': 'application/json'
    }
    body = {
        "availability": {
            "shipToLocationAvailability": {
                "quantity": 50
            }
        },
        "condition": "NEW",
        "product": {
            "title": "GoPro Hero4 Helmet Cam",
            "description": "New GoPro Hero4 Helmet Cam. Unopened box.",
            "aspects": {
                "Brand": [
                    "GoPro"
                ],
                "Type": [
                    "Helmet/Action"
                ],
                "Storage Type": [
                    "Removable"
                ],
                "Recording Definition": [
                    "High Definition"
                ],
                "Media Format": [
                    "Flash Drive (SSD)"
                ],
                "Optical Zoom": [
                    "10x"
                ]
            },
            "brand": "GoPro",
            "mpn": "CHDHX-401",
            "imageUrls": [
                "http://i.ebayimg.com/images/i/182196556219-0-1/s-l1000.jpg",
                "http://i.ebayimg.com/images/i/182196556219-0-1/s-l1001.jpg",
                "http://i.ebayimg.com/images/i/182196556219-0-1/s-l1002.jpg"
            ]
        }
    }

    r = requests.put(url, headers=headers, params=body)
    print(r.json())

create_item()