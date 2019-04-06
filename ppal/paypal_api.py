import requests


class PaypalApi:
    base = 'https://api.sandbox.paypal.com/v2'
    access_token = 'A21AAFv3KFHpxUZHP_kwx9dYpe318JqZ3otuFc7bJn97XkC7WPkTCPcd9RiNOmrc3GVvJrf8z6pnMyhQAD7d0X_E9iqT7J2SQ'

    secret_id = "EGXQU-Gt2i6_fYqDIUOl0bkuEjsCpQMNezyaCCqTGd5ZD0giuwb3w_CkOx65hyYSGMQleqCncwp8ogwL"
    client_id = "AV34qXNy1vUTzCjKGSX-uCuc-VheuKQmU4f-Et8PQviy93tju5v_1UE4uZiHPZB72d0fV-qx0zJvkScZ"
    auth = f"Bearer {access_token}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": auth,
    }

    def get_order(self, order_id):
        url = f'{self.base}/checkout/orders/{order_id}'

        r = requests.get(url, headers=self.headers)
        return r.json()

    def get_access_token(self):
        url = "https://api.sandbox.paypal.com/v1/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US",
        }

        params = {
            "grant_type": "client_credentials"
        }
        r = requests.post(url, headers=headers, data=params, auth=(self.client_id, self.secret_id))
        return r.json()

