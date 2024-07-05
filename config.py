from pathlib import Path

TOKEN = '7407700588:AAEbBXJHDBiVeTLkekuJ_4DzoTz_eJxjcBQ'

CREDENTIALS = str(Path(str(Path.cwd()), 'google_sheet', 'credentials.json'))

CATEGORY = {
    'Одежда 👗': [
            {
                'Accept': '*/*',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'Origin': 'https://www.wildberries.ru',
                'Referer': 'https://www.wildberries.ru/catalog/muzhchinam/ofis?sort=popular&page=_edit_page_',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 OPR/89.0.4447.64 (Edition Yx GX)',
                'sec-ch-ua': '"Opera GX";v="89", "Chromium";v="103", "_Not:A-Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            },

            'https://catalog.wb.ru/catalog/men_clothes/catalog?appType=1&couponsGeo=10,2,12,7,3,18,21&curr=rub&dest=-1029256,-2095259,-570649,-3313072&emp=0&ext=31140&kind=1&lang=ru&locale=ru&page=_edit_page_&pricemarginCoeff=1.0&reg=1&regions=68,64,83,4,38,80,33,70,82,86,30,69,22,66,31,40,1,48&sort=popular&spp=22&subject=11;149;156;160;177;184;191;215'
    ],

    'Книги 📚':[
            {
                'Accept': '*/*',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'Origin': 'https://www.wildberries.ru',
                'Referer': 'https://www.wildberries.ru/catalog/knigi/hudozhestvennaya-literatura?sort=popular&cardsize=c516x688&page=_edit_page_',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 OPR/89.0.4447.64 (Edition Yx GX)',
                'sec-ch-ua': '"Opera GX";v="89", "Chromium";v="103", "_Not:A-Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            },

            'https://catalog.wb.ru/catalog/books_fiction/catalog?appType=1&couponsGeo=10,2,12,7,3,18,21&curr=rub&dest=-1029256,-2095259,-570649,-3313072&emp=0&ext=69439;69444;69449;69455;69457;69459;69473;69479;69487;70848;155767;205607&lang=ru&locale=ru&page=_edit_page_&pricemarginCoeff=1.0&reg=1&regions=68,64,83,4,38,80,33,70,82,86,30,69,22,66,31,40,1,48&sort=popular&spp=22&subject=381;4961;5805'

    ],

    'Смартфоны 📱':[
            {
                'Accept': '*/*',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'Origin': 'https://www.wildberries.ru',
                'Referer': 'https://www.wildberries.ru/catalog/elektronika/smartfony-i-telefony/vse-smartfony?sort=popular&cardSize=c516x688&page=_edit_page_',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 OPR/89.0.4447.64 (Edition Yx GX)',
                'sec-ch-ua': '"Opera GX";v="89", "Chromium";v="103", "_Not:A-Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            },

            'https://catalog.wb.ru/catalog/electronic3/catalog?appType=1&couponsGeo=10,2,12,7,3,18,21&curr=rub&dest=-1029256,-2095259,-570649,-3313072&emp=0&lang=ru&locale=ru&page=_edit_page_&pricemarginCoeff=1.0&reg=1&regions=68,64,83,4,38,80,33,70,82,86,30,69,22,66,31,40,1,48&sort=popular&spp=22&subject=515'
    ]
}

HEADERS_TIME = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Origin': 'https://www.wildberries.ru',
    'Referer': 'https://www.wildberries.ru/catalog/0/search.aspx?page=_edit_page_&sort=popular&search=_replace_me_',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 OPR/89.0.4447.64 (Edition Yx GX)',
    'sec-ch-ua': '"Opera GX";v="89", "Chromium";v="103", "_Not:A-Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}



