import re
from time import sleep

from bs4 import BeautifulSoup as B
from decouple import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class TcgScraper:
    def __init__(self):
        self.GOOGLE_CHROME_BIN = config('GOOGLE_CHROME_BIN')
        self.GOOGLE_CHROME_SHIM = config('GOOGLE_CHROME_SHIM')
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument("headless")
        self.chrome_options.binary_location = self.GOOGLE_CHROME_BIN
        self.driver = webdriver.Chrome(self.GOOGLE_CHROME_SHIM, options=self.chrome_options)

    def quit_driver(self):
        self.driver.quit()

    def query(self, value):
        if value is not None:
            self.driver.execute_script("$(arguments[0]).click();", value)
        else:
            return 'Error in value'

    def get_url(self, url):
        self.driver.get(url)

    def open_filters(self):
        self.driver.find_element_by_xpath('//*[@id="product-price-table"]/div[1]/button').click()

    def get_card_data(self, query_condition):
        sleep(5)
        page_source = self.driver.page_source
        soup = B(page_source, 'html.parser')
        cards = soup.find_all('div', {'class': 'product-listing'})
        seller_data_list = []
        for card in cards:
            condition = card.find('a', {'class': 'condition'}).text
            if query_condition == condition:
                seller_name = card.find('a', {'class': 'seller__name'}).text.strip()
                if seller_name != 'Moose Loot' and seller_name != 'Moose Loot Direct':
                    total_sales = card.find('span', {'class': 'seller__sales'}).text
                    total_sales = [i for i in total_sales if i.isnumeric()]
                    total_sales = int(''.join(total_sales))
                    price = card.find('span', {'class': 'product-listing__price'}).text.strip('$')
                    shipping_string = card.find('span', {'class': 'product-listing__shipping'}).text
                    if 'included' in shipping_string.lower():
                        shipping = 0
                    else:
                        shipping = re.findall(r"[-+]?\d*\.\d+|\d+", shipping_string)
                        shipping = ''.join(shipping)

                    total_price = float(price) + float(shipping)

                    seller_data_list.append(
                        {
                            'price': total_price,
                            'gold': True if total_sales >= 10000 else False,
                        }
                    )
                    if len(seller_data_list) == 5:
                        break
                else:
                    # Filter for query failed for some reason
                    print('Query Failed')

        return seller_data_list

    def filter_value(self, query):

        q = {
            'next_page': self.driver.find_element_by_xpath('//*[@id="priceTableContainer"]/div/nav/ul/a[4]'),
            'Near Mint': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[5]/li[2]/a'),
            'Lightly Played': self.driver.find_element_by_xpath('//*[''@id="detailsFilters"]/div/div/ul[5]/li[3]/a'),
            'Moderately Played': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[5]/li[4]/a'),
            'Heavily Played': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[5]/li[5]/a'),
            'Damaged': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[5]/li[6]/a'),
            'Unopened': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[5]/li[7]/a'),
            'Normal': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[4]/li[2]/a'),
            'Foil':  self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[4]/li[3]/a'),
            'four_or_more': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[2]/li[2]/a'),
            'English': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[6]/li[2]/a'),
            'Chinese (S)': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[6]/li[3]/a'),
            'all_non_english': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[6]/li[4]/a'),
            'Chinese (T)': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[6]/li[5]/a'),
            'French': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[6]/li[6]/a'),
            'German': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[6]/li[7]/a'),
            'Italian': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[6]/li[8]/a'),
            'Japanese': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[6]/li[9]/a'),
            'Korean': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[6]/li[10]/a'),
            'Portuguese': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[6]/li[11]/a'),
            'Russian': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[6]/li[12]/a'),
            'Spanish': self.driver.find_element_by_xpath('//*[@id="detailsFilters"]/div/div/ul[6]/li[13]/a'),
        }

        return q.get(query)




