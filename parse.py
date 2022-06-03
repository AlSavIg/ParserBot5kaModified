import datetime
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import aiofiles
import asyncio
from aiocsv import AsyncWriter

selected_store_names = {
    '28870': 'Косыгина, 31',
    '7215': 'Наставников пр, 3',
    '7179': 'Садовая, 69 лит.А'
}


async def collect_data(shop_id):
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

    selected_store = {
        '28870':
            '{"id": 28870,'
            '"sap_code": "33YU",'
            '"address": "г.Санкт-Петербург, пр-кт Косыгина, 31",'
            '"work_start_time": "08:00:00",'
            '"work_end_time": "23:00:00",'
            '"is_24h": false};',
        '7215':
            '{"id": 7215,'
            '"sap_code": "5677",'
            '"address": "г.Санкт-Петербург, Наставников пр, 3",'
            '"work_start_time": "09:00:00",'
            '"work_end_time": "23:00:00",'
            '"is_24h": false};',
        '7179':
            '{"id": 7179, '
            '"sap_code": "5593", '
            '"address": "г.Санкт-Петербург, ул. Садовая, 69 лит.А",'
            '"work_start_time": null, '
            '"work_end_time": null, '
            '"is_24h": false};'
    }

    headers = {
        'User-Agent': UserAgent().random
    }

    cookies = {
            'selectedStore': f'{selected_store[shop_id]}'.encode('utf-8').decode('latin-1')
    }
    response = requests.get(url='https://5ka.ru/special_offers', headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'lxml')

    cards = soup.find_all("div", {'class': 'product-card item'})

    data = []
    for card in cards:
        card_name = card.find('div', {'class': 'item-name'}).get_text(strip=True)

        card_price = card.find('div', {'class': 'price-discount'})

        card_discount_int = card_price.find('span').get_text(strip=True)
        card_discount_dec = card_price.find('div', {'class': 'price-right'})\
            .find('span', {'class': 'price-discount_cents'}).get_text(strip=True)
        card_discount_price = f'{card_discount_int}.{card_discount_dec}'

        card_old_price = card_price.find('div', {'class': 'price-right'})\
            .find('span', {'class': 'price-regular'}).get_text(strip=True)

        card_discount = card.find('div', {'class': 'discount-hint hint'}).get_text(strip=True).replace('-', '')

        card_sale_date = card.find('div', {'class': 'item-date'}).get_text(strip=True)

        data.append([card_name, card_discount_price, card_discount, card_old_price, card_sale_date])

    async with aiofiles.open(f'{selected_store_names[shop_id]}_{cur_time}.csv', 'w',
                             encoding='utf-8',
                             newline='') as file:
        writer = AsyncWriter(file)

        await writer.writerow(
            [
                'Продукт',
                'Новая цена',
                'Скидка',
                'Старая цена',
                'Период акции',
            ]
        )
        await writer.writerows(data)

    return f'{selected_store_names[shop_id]}_{cur_time}.csv'


async def main():
    await collect_data(shop_id='7179')


if __name__ == '__main__':
    asyncio.run(main())
