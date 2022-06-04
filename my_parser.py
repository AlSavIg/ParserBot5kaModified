import datetime
import webbrowser

import requests
import aiofiles
import asyncio
from aiocsv import AsyncWriter
from stores import selected_stores

items_on_page = 30
page = 1
url = 'EMPTY'


def get_data(local_url):
    response = requests.get(url=local_url)
    data = response.json()
    data_container = []
    while data.get('next') is not None:
        local_url = data.get('next')
        results = data.get('results')
        for item in results:
            parsed_data = data_collector(item)
            data_container.append(parsed_data)
        response = requests.get(url=local_url)
        data = response.json()
    return data_container


def data_collector(item):
    name = item.get('name')
    img_link = item.get('img_link')
    promo_date_begin = item.get('promo').get('date_begin')
    promo_date_end = item.get('promo').get('date_end')
    promo_date = f'{promo_date_begin} - {promo_date_end}'
    old_price = item.get('current_prices').get('price_reg__min')
    new_price = item.get('current_prices').get('price_promo__min')
    discount = f'{round((1 - new_price / old_price) * 100)}%'
    return [name,
            img_link,
            promo_date,
            old_price,
            new_price,
            discount]


async def collect_data(shop_id):
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    global url
    url = 'https://5ka.ru/api/v2/special_offers/' \
          f'?records_per_page={items_on_page}' \
          f'&page={page}' \
          f'&store={shop_id}' \
          '&ordering=' \
          '&price_promo__gte=' \
          '&price_promo__lte=' \
          '&categories=' \
          '&search='

    data = get_data(local_url=url)

    async with aiofiles.open(f'{selected_stores[shop_id]}_{cur_time}.csv', 'w',
                             encoding='utf-8',
                             newline='') as file:
        writer = AsyncWriter(file)

        await writer.writerow(
            [
                'Наименование',
                'Ссылка_на_изображение',
                'Период_акции',
                'Старая_цена',
                'Новая_цена',
                'Скидка'
            ]
        )
        await writer.writerows(data)

    return f'{selected_stores[shop_id]}_{cur_time}.csv'


async def main():
    await collect_data(shop_id='5600')


if __name__ == '__main__':
    asyncio.run(main())
