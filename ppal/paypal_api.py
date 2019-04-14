import requests
from .models import PaypalAccessToken


class PaypalApi:
    base = 'https://api.paypal.com/v2'

    secret_id = "EHHFfW_-beWG8DqrizqNeed1XZHA4fnNFEaOMzm2e7MMP0OFsvB2bweu4cuKxr5It9PkkT3cPiU3gXJe"
    client_id = "AeQOEmoEfAZov4p3r2FvIgF3CLCFJ96oMnxGc2nobxX7I8hLQgP67Yl4ULDX74mT_E68Ok1Zk_fQCV6p"

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
            "grant_type": "client_credentials"
        }
        r = requests.post(url, headers=headers, data=params, auth=(self.client_id, self.secret_id)).json()
        paypal_credentials = PaypalAccessToken.objects.first()
        paypal_credentials.access_token = r['access_token']
        paypal_credentials.app_id = r['app_id']
        paypal_credentials.nonce = r['nonce']
        paypal_credentials.save()

