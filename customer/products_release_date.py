from bs4 import BeautifulSoup as B
import requests
from .models import ReleasedProducts
from customer.fix_words import FixWords
from datetime import date

fix = FixWords()

"""payload = {'email_address': 'nsaverino@gmail.com', 'password': 'Dominaria1!', '':'Log In'}
login_url = 'https://www.southernhobby.com/login.php?action=process'
url = 'https://www.southernhobby.com/ccg-s/magic-the-gathering/c13_362/'

with requests.session() as s:
    s.get(login_url)
    s.post(login_url, data=payload)
    response = s.get(url)
    print(response.text)"""


"""with requests.session() as s:

    ### Here, we're getting the login page and then grabbing hidden form
    ### fields.  We're probably also getting several session cookies too.
    login = s.get('https://www.southernhobby.com/login.php?action=process')


    login_html = lxml.html.fromstring(login.text)
    hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
    form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
    form['email'] = 'nsaverino@gmail.com'
    form['password'] = 'Dominaria1!'

    response = s.post('https://www.southernhobby.com/login.php?action=process', data=form)
    cookies = s.cookies
    print(cookies)
    print(response.url)"""

def mtg():
    current_items = ReleasedProducts.objects.values_list('product', flat=True)
    origin_url = 'https://wpn.wizards.com/en/products'
    r = requests.get(origin_url).content
    soup = B(r, 'html.parser')
    links = soup.find_all('div', {'class': 'view-content'})
    urls_list = []
    for each in links:
        x = each.find_all('div', {'class': 'views-field views-field-field-brand'})
        y = each.find_all('div', {'class': 'views-field views-field-field-hero-image'})
        for card, type in zip(y, x):
            if 'Magic: The Gathering' in type.div.text:
                urls_list.append('https://wpn.wizards.com/'+card.a.get('href'))

    urls_list = list(set(urls_list))

    count = 0
    while count < len(urls_list):

        r = requests.get(urls_list[count]).content
        soup = B(r, 'html.parser')
        test = 0
        while True:
            product = soup.find_all('div', {'id': 'field-products-section-tab-' + str(test)})
            if len(product) > 0:
                for each in product:
                    try:
                        release_date = each.find('div', {'class': 'field field-name-field-product-c-release-date-txt field-type-text field-label-inline clearfix'}).div.next_sibling.text
                    except AttributeError:
                        date_info = soup.find('div', {'class': 'product-release date-container'})
                        if date_info == None or date_info == 'None':
                            release_date = 'Unknown'
                        else:
                            release_date = date_info.span.text
                    month = fix.fix_month(release_date.lower())
                    year = release_date[-4:]
                    if year[0:2] != '20':
                        year = date.today().year
                    product_name = each.find('div', {'class': 'field-items'}).div.text
                    msrp = each.find('div', {'class': 'field field-name-field-product-c-msrp field-type-text field-label-above'}).find('div', {'class': 'field-item'}).text

                    if product_name not in current_items:
                        new_product = ReleasedProducts(
                            product=product_name, release_date=release_date, price=msrp, link=urls_list[count], month=month, year=year
                        )
                        new_product.save()
                test += 1
            else:
                break
        count += 1
