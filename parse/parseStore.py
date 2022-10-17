import difflib
import json
import re
import string

import requests
from bs4 import BeautifulSoup

from productData import ResponseProduct, StoreFields

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
}


def get_html(data, search, retry=0) -> ResponseProduct:
    utl = data[StoreFields.URL]
    try:
        response = requests.get(url=utl, headers=headers)
        print(f"[+] {utl} {response.status_code}")
    except Exception as ex:
        if retry:
            print(f"[INFO] retry={retry} => {utl}")
            return get_html(data, search, (retry - 1))
        else:
            raise ex
    else:
        if response.status_code != 200 and retry:
            print(f"[INFO] retry={retry} => {utl}")
            return get_html(data, search, (retry - 1))
        else:
            return get_data(data, search, response.text)


def get_data(data, search, html) -> ResponseProduct:
    soup = BeautifulSoup(html, 'lxml')
    price = soup.select(data[StoreFields.PRICE_CLASS])
    name = soup.find(class_=data[StoreFields.NAME_CLASS])
    url_link = soup.find(class_=data[StoreFields.LINK_URL])
    if url_link is not None:
        url_link = data[StoreFields.BASE_URL] + url_link["href"]
        if len(price) > 0:
            price = re.sub('[^0-9]', '', price[0].text)
        if name is not None:
            name = name.text.replace("\n", "")
    product = ResponseProduct(name, price, url_link)

    if data[StoreFields.STORE] == "Notik":
        product = check_notik(data, soup, search)
    if data[StoreFields.STORE] == "BigGeek":
        product = check_big_geek(data, html, search)

    return product


def check_notik(data, soup, search):
    products = dict()
    url_links = soup.select(data[StoreFields.LINK_URL])
    i = -1
    for product in soup.select(data[StoreFields.SELECTOR]):
        price = product[data[StoreFields.PRICE_CLASS]]
        name = product[data[StoreFields.NAME_CLASS]]
        url_link = data[StoreFields.BASE_URL] + url_links[++i]["href"]
        products[similarity(name, search)] = ResponseProduct(name, price, url_link)
    sort = sorted(products.items(), reverse=True)
    if len(sort) > 0:
        return sort[0][1]
    return ResponseProduct()


def check_big_geek(data, html, search) -> ResponseProduct:
    data_json = json.loads(html)
    products = dict()
    for data_products in data_json[data[StoreFields.SELECTOR]]:
        price = data_products[data[StoreFields.PRICE_CLASS]]
        name = data_products[data[StoreFields.NAME_CLASS]]
        url_link = data[StoreFields.BASE_URL]  + data_products[data[StoreFields.LINK_URL]]
        products[similarity(name, search)] = ResponseProduct(name, price, url_link)
    sort = sorted(products.items(), reverse=True)
    if len(sort) > 0:
        return sort[0][1]
    return ResponseProduct()


def similarity(s1: string, s2: string) -> float:
    if len(s1) == 0 or len(s2) == 0:
        return 0
    return difflib.SequenceMatcher(None, s1.lower(), s2.lower()).ratio()
