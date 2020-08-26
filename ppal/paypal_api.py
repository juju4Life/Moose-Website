import requests
from .models import PaypalAccessToken
from decouple import config


class PaypalApi:
    base = 'https://api.paypal.com/v2'

    secret_id = config('paypal_secret_id')
    client_id = config('paypal_client_id')

    def get_headers(self, access_token):
        auth = f"Bearer {access_token}"
        headers = {

            "Content-Type": "application/json",
            "Authorization": auth,
        }

        return headers

    def get_order(self, order_id):
        url = f'{self.base}/checkout/orders/{order_id}'
        access_token = PaypalAccessToken.objects.first().access_token
        r = requests.get(url, headers=self.get_headers(access_token))
        return r.json()

    def get_access_token(self):
        url = "https://api.paypal.com/v1/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US",
        }

        params = {
            "grant_type": "client_credentials",
        }
        r = requests.post(url, headers=headers, data=params, auth=(self.client_id, self.secret_id)).json()
        paypal_credentials = PaypalAccessToken.objects.first()
        paypal_credentials.access_token = r['access_token']
        paypal_credentials.app_id = r['app_id']
        paypal_credentials.nonce = r['nonce']
        paypal_credentials.save()

