from .models import TcgCredentials
import requests


class Credentials:
    bearer_tokens = {
        'first': TcgCredentials.objects.get(name='first').token,
        'moose': TcgCredentials.objects.get(name='moose').token,
    }
    content_type = "application/json"
    first_store_key = "399a7564"
    moose_store_key = "72a0d337"

    store_keys = {
        'first': first_store_key,
        'moose': moose_store_key,
    }
    token = "39cf2a47-1de8-43ad-b29c-1542a670ccd8"
    public_key = "071BA187-6E51-4A3F-A2AF-C1C27663B543"
    private_key = "DEBC2A03-0DDF-4CDE-8755-91CB1947A16B"
    url = 'https://api.tcgplayer.com/v1.39.0/'
    payload = "grant_type=client_credentials&client_id=" + public_key + "&client_secret=" + private_key

    def get_request_with_params(self, url, store, **kwargs):
        path = self.url + url
        headers = {
            "Accept": self.content_type,
            "Authorization": "bearer " + self.bearer_tokens[store],
            "Content-Type": self.content_type,
        }
        try:
            r = requests.get(path, params=kwargs['params'], headers=headers, data=kwargs)
            return r.json()
        except requests.exceptions.ConnectionError as e:
            print(e)

    def get_request(self, url, store, **kwargs):
        path = self.url + url
        headers = {
            "Accept": self.content_type,
            "Authorization": "bearer " + self.bearer_tokens[store],
            "Content-Type": self.content_type,
        }
        try:
            if kwargs:
                r = requests.get(path, headers=headers, params=kwargs['params'])
            else:
                r = requests.get(path, headers=headers)

            return r.json()
        except requests.exceptions.ConnectionError as e:
            print(e)

    def post_data(self, url, store, data):
        path = self.url + url
        headers = {
            "Accept": self.content_type,
            "Authorization": "bearer " + self.bearer_tokens[store],
            "Content-Type": self.content_type,
        }
        r = requests.post(url=path, headers=headers, data=data)

        return r.json()

    def post_request(self, url, store, data):
        path = self.url + url
        headers = {
            "Accept": self.content_type,
            "Authorization": "bearer " + self.bearer_tokens[store],
            "Content-Type": self.content_type,
        }

        try:
            r = requests.post(path, headers=headers, json=data)
            return r.json()
        except requests.exceptions.ConnectionError as e:
            print(e)

    def put_request(self, url, store, _data, _json, **kwargs):
        path = self.url + url
        headers = {
            "Accept": self.content_type,
            "Authorization": "bearer " + self.bearer_tokens[store],
            "Content-Type": self.content_type,
        }

        try:
            if _json is True:
                r = requests.put(path, headers=headers, json=kwargs['json'])
                data = r.json()
                return data
            elif _data is True:
                r = requests.put(path, headers=headers, data=str(kwargs['data']))
                return r.json()

        except requests.exceptions.ConnectionError as e:
            print(e)

    def new_bearer_token(self):
        import requests

        first_access_token = "39cf2a47-1de8-43ad-b29c-1542a670ccd8"
        moose_access_token = "f53c8f0d-a7b3-48c1-bde1-9fbdd8605ad7"
        public_key = "071BA187-6E51-4A3F-A2AF-C1C27663B543"
        private_key = "DEBC2A03-0DDF-4CDE-8755-91CB1947A16B"
        payload = "grant_type=client_credentials&client_id=" + public_key + "&client_secret=" + private_key

        first_headers = {
            "Content-Type": self.content_type,
            "Accept": self.content_type,
            "X-Tcg-Access-Token": first_access_token,
        }

        moose_headers = {
            "Content-Type": self.content_type,
            "Accept": self.content_type,
            "X-Tcg-Access-Token": moose_access_token,
        }

        url = "https://api.tcgplayer.com/token"
        first_token = TcgCredentials.objects.get(name='first')
        moose_token = TcgCredentials.objects.get(name='moose')
        r_first = requests.post(url, headers=first_headers, data=payload).json()
        r_moose = requests.post(url, headers=moose_headers, data=payload).json()
        first_token.token = r_first['access_token']
        moose_token.token = r_moose['access_token']
        first_token.save()
        moose_token.save()



