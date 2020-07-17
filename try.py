import requests

data = {
  'hub.mode': 'subscribe',
  'hub.topic': 'https://magic.wizards.com/en/rss/rss.xml?tags=Daily MTG',
  'lang': 'en',
  'hub.callback': 'https://www.tcgfirst.com/layout/hook',
  'hub.secret': 'c49e102b-71af-429d-a758-8edcb15229b9',
  'hub.verify': 'sync',
  'format': 'json'
}

response = requests.post('https://push.superfeedr.com/', data=data, auth=('mooseloot', '7ee4a8f1c8907e52e481af220f51e27d'))

