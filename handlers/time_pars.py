import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import config as cfg

import urllib.parse

from pathlib import Path

from database.sqlite_db import Database




def request_session():
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5, total=15)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session


def get_data(name):
    name_products = name.replace(' ', '+')
    name_products_en = urllib.parse.quote(name_products)
    name_en = urllib.parse.quote(name)

    dict_products = {'prod': []}
    page = 1
    while True:
        cfg.HEADERS_TIME['Referer'] = cfg.HEADERS_TIME['Referer'].replace('_replace_me_', name_products_en).replace(
            '_edit_page_', str(page))

        url = 'https://search.wb.ru/exactmatch/ru/male/v4/search?appType=1&couponsGeo=10,2,12,7,3,18,21&curr=rub&dest=-1029256,-2095259,-570649,-3313072&emp=0&lang=ru&locale=ru&page=_edit_page_&pricemarginCoeff=1.0&query=_replace_me_&reg=1&regions=68,64,83,4,38,80,33,70,82,86,30,69,22,66,31,40,1,48&resultset=catalog&sort=popular&spp=20&suppressSpellcheck=false'
        url_en = url.replace('_replace_me_', name_en).replace('_edit_page_', str(page))

        response = request_session().get(url_en, headers=cfg.HEADERS_TIME).json()
        if (response is None) or response == {}:
            break
        else:
            if response.get('data').get('products') == [] or response.get('data').get('products') == {}:
                break

        for i in range(len(response.get('data').get('products'))):

            link = f'https://www.wildberries.ru/catalog/{response.get("data").get("products")[i].get("id")}/detail.aspx?targetUrl=IM'

            if name.lower() in response.get('data').get('products')[i].get('name').lower():
                dict_products['prod'].append({
                    'name': response.get('data').get('products')[i].get('name').lower(),
                    'price': int(int(response.get('data').get('products')[i].get('salePriceU')) / 100),
                    'link': link
                })

        page += 1
    if dict_products['prod'] == []:
        return False
    else:
        return dict_products




need_prod = []
def find_user_opt_time(string, price, tgid):
    dir_path = str(Path.cwd())
    path_to_db = str(Path(dir_path, 'google_parser.db'))
    db = Database(path_to_db)

    global need_prod
    db.update_parsing_status(tgid, 1)
    price_list = price.split('-')
    if get_data(string):
        name = string.lower()
        for product in get_data(name).get('prod'):
            name_product = product.get('name')
            price = product.get('price')
            link = product.get('link')
            if (name in name_product) and (int(price_list[0]) <= int(price) <= int(price_list[1])):
                need_prod.append(link)
        if need_prod == []:
            db.update_parsing_status(tgid, 0)
            need_prod = [False]
    else:
        db.update_parsing_status(tgid, 0)
        need_prod = [False]
    db.update_parsing_status(tgid, 0)

async def return_links_time_pars():
    return need_prod

async def clear_links_time_pars():
    need_prod.clear()





def find_min_price(string, tgid):
    dir_path = str(Path.cwd())
    path_to_db = str(Path(dir_path, 'google_parser.db'))
    db = Database(path_to_db)

    global minimum_price
    db.update_parsing_status(tgid, 1)
    if get_data(string):
        name = string.lower()
        data = get_data(name).get('prod')
        price_list = []
        for prod in data:
            if name in prod.get('name'):
                price_list.append(prod.get('price'))
        try:
            min(price_list)
        except ValueError:
            db.update_parsing_status(tgid, 0)
            minimum_price = [False]
        else:
            min_price = min(price_list)
            index = 0
            counter = 0
            for product in range(len(data)):
                if min_price == data[counter].get('price'):
                    index = counter
                counter += 1

            price = data[index].get('price')
            link = data[index].get('link')
            db.update_parsing_status(tgid, 0)
            minimum_price = [True, price, link]

    else:
        minimum_price = [False]
        db.update_parsing_status(tgid, 0)
    db.update_parsing_status(tgid, 0)


async def return_min_price():
    return minimum_price


async def clear_min_price():
    minimum_price.clear()
