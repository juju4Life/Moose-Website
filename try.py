import requests


def create_feed(topic):
    data = {
        'hub.mode': 'subscribe',
        'hub.topic': topic,
        'lang': 'en',
        'hub.callback': 'https://www.tcgfirst.com/layout/hook',
        'hub.secret': 'c49e102b-71af-429d-a758-8edcb15229b9',
        'hub.verify': 'sync',
        'format': 'json'
    }

    response = requests.post('https://push.superfeedr.com/', data=data, auth=('mooseloot', '7ee4a8f1c8907e52e481af220f51e27d'))

    print(response)


create_feed("http://push-pub.appspot.com/")

