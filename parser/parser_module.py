import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


from bs4 import BeautifulSoup

import config as cfg

from database.sqlite_db import Database

from pathlib import Path




def request_session():
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5, total=15)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session


def get_ids(page, category_user):
    counter = 0
    for page in range(1, int(page)+1):
        referrer = cfg.CATEGORY[category_user][0]['Referer'].replace('_edit_page_', str(page))
        headers = cfg.CATEGORY[category_user][0]
        headers['Referer'] = referrer
        url = cfg.CATEGORY[category_user][1].replace('_edit_page_', str(page))

        response = request_session().get(url, headers=headers).json()


        products = response.get('data').get('products')

        for prod in products:
            product_id = prod.get('id')
            product_part = str(product_id)[0:len(str(product_id)) - 3]

            print('[!] Загрузка... ', counter)
            counter += 1
            yield product_id, product_part





def find_errors(image_link):
    response = request_session().get(image_link)

    soup = BeautifulSoup(response.text, 'lxml')

    success = soup.find('head')
    return success



def check_image_link(image_link):
    if find_errors(image_link):
        for i in range(1, 100):
            new_link = image_link.replace('https://basket-02.wb.ru', f'https://basket-0{i}.wb.ru')
            if find_errors(new_link):
                continue
            else:
                return new_link
                break
    else:
        return image_link



def get_data(list_ids, page, category, tgid):

    dir_path = str(Path.cwd())
    path_to_db = str(Path(dir_path, 'google_parser.db'))
    db = Database(path_to_db)
    db.update_parsing_status(tgid, 1)

    if get_ids(page, category):
        errors = []
        for id in list_ids:
            try:
                response = request_session().get(f'https://wbx-content-v2.wbstatic.net/ru/{id[0]}.json').json()
            except:
                print('[!] Ошибочка')
                errors.append(id[0])
                continue

            headers = {
                'Accept': '*/*',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'Origin': 'https://www.wildberries.ru',
                'Referer': f'https://www.wildberries.ru/catalog/{id[0]}/detail.aspx?targetUrl=GP',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.85 (Edition Yx GX)',
                'sec-ch-ua': '"Chromium";v="102", "Opera GX";v="88", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }

            try:
                result = request_session().get(
                    f'https://card.wb.ru/cards/detail?spp=17&regions=68,64,83,4,38,80,33,70,82,86,30,69,22,66,31,40,1,48&pricemarginCoeff=1.0&reg=1&appType=1&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=10,2,12,7,3,18,21&dest=-1029256,-2095259,-570649,-3313072&nm={id[0]}',
                    headers=headers).json()
            except:
                print('[!] Ошибочка_2')
                errors.append(id[0])
                continue


            name = response.get('imt_name')
            description = response.get('description')
            image_link = f'https://basket-02.wb.ru/vol{str(id[0])[:len(str(id[0])) - 5]}/part{id[1]}/{id[0]}/images/c516x688/1.jpg'

            image_link = check_image_link(image_link)
            basePrice = int(int(result.get('data').get('products')[0].get('salePriceU')) / 100)
            salePrice = int(int(result.get('data').get('products')[0].get('priceU')) / 100)

            yield name, salePrice, basePrice, image_link, category

        db.update_parsing_status(tgid, 0)














