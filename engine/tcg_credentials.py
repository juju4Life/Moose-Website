from .models import TcgCredentials
import requests


class Credentials:
    bearer_token = TcgCredentials.objects.get(name='').token
    content_type = "application/json"
    store_key = "399a7564"
    token = "39cf2a47-1de8-43ad-b29c-1542a670ccd8"
    public_key = "071BA187-6E51-4A3F-A2AF-C1C27663B543"
    private_key = "DEBC2A03-0DDF-4CDE-8755-91CB1947A16B"
    url = 'http://api.tcgplayer.com/v1.19.0/'
    payload = "grant_type=client_credentials&client_id=" + public_key + "&client_secret=" + private_key

    headers = {
        "Accept": content_type,
        "Authorization": "bearer " + bearer_token,
        "Content-Type": content_type,
    }

    def get_request_with_params(self, url, **kwargs):
        path = self.url + url
        try:
            r = requests.get(path, params=kwargs['params'], headers=self.headers, data=kwargs)
            return r.json()
        except requests.exceptions.ConnectionError as e:
            print(e)

    def get_request(self, url, **kwargs):
        path = self.url + url
        try:
            if kwargs:
                r = requests.get(path, headers=self.headers, params=kwargs['params'])
            else:
                r = requests.get(path, headers=self.headers)

            return r.json()
        except requests.exceptions.ConnectionError as e:
            print(e)

    def post_request(self, url, data):
        path = self.url + url
        print(data)
        try:
            r = requests.post(path, headers=self.headers, json=data)
            return r.json()
        except requests.exceptions.ConnectionError as e:
            print(e)

    def put_request(self, url, _data, _json, **kwargs):
        path = self.url + url
        try:
            if _json is True:
                r = requests.put(path, headers=self.headers, json=kwargs['json'])
                return r.json()
            elif _data is True:
                r = requests.put(path, headers=self.headers, data=str(kwargs['data']))
                return r.json()

        except requests.exceptions.ConnectionError as e:
            print(e)

    def new_bearer_token(self):
        import requests

        token = "39cf2a47-1de8-43ad-b29c-1542a670ccd8"
        public_key = "071BA187-6E51-4A3F-A2AF-C1C27663B543"
        private_key = "DEBC2A03-0DDF-4CDE-8755-91CB1947A16B"
        payload = "grant_type=client_credentials&client_id=" + public_key + "&client_secret=" + private_key

        headers = {
            "Content-Type": self.content_type,
            "Accept": self.content_type,
            "X-Tcg-Access-Token": token,
        }

        url = "https://api.tcgplayer.com/token"
        old_token = TcgCredentials.objects.get(name='')
        r = requests.post(url, headers=headers, data=payload).json()
        old_token.token = r['access_token']
        old_token.save()



