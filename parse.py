import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import aiohttp
import aiofiles
import asyncio
from aiocsv import AsyncWriter


async def collect_data(shop_id):
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    ua = UserAgent()

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
            '"is_24h": false};'
    }

    selected_store_names = {
        '28870': 'Косыгина, 31',
        '7215': 'Наставников пр, 3'
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua.random
    }

    cookies = {
    #     'selectedStore': f'{selected_store[shop_id]}'

    #     'selectedStore': '%7B%22id%22%3A28870%2C%22sap_code%22%3A%2233YU%22%2C%22address%22%3A%22%D0%B3.%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%2C%20%D0%BF%D1%80-%D0%BA%D1%82%20%D0%9A%D0%BE%D1%81%D1%8B%D0%B3%D0%B8%D0%BD%D0%B0%2C%2031%22%2C%22work_start_time%22%3A%2208%3A00%3A00%22%2C%22work_end_time%22%3A%2223%3A00%3A00%22%2C%22is_24h%22%3Afalse%7D"'
    }

    async with aiohttp.ClientSession() as session:

        response = await session.get(url='https://5ka.ru/special_offers', headers=headers, cookies=cookies)
        soup = BeautifulSoup(await response.text(), 'lxml')

        cards = soup.find_all("div", {'class': 'product-card item'})

        data = []
        for card in cards:
            print(card)
            card_name = card.find('div', {'class': 'item-name'}).get_text(strip=True)

            card_price = card.find('div', {'class': 'prices'}).find('div', {'class': 'price-discount'})

            print('\n')

            print(card_price)

            card_discount_int = card_price.find('span').get_text(strip=True)
            card_discount_dec = card_price.find('div', {'class': 'price-right'})\
                .find('span', {'class': 'price-discount_cents'}).get_text(strip=True)
            card_price_old_int = card_price.find('div', {'class': 'price-right'})\
                .find('span', {'class': 'price-regular'}).get_text(strip=True)
            card_price_old_dec = card_price.find('sup').get_text(strip=True)

            card_old_price = f'{card_price_old_int}.{card_price_old_dec}'
            card_discount_price = f'{card_discount_int}.{card_discount_dec}'
            # card_discount = f'{round(int(card_discount_price) / int(card_old_price), 4)  * 100}%'

            card_sale_date = card.find('div', {'class': 'item-date'}).get_text(strip=True)

            data.append([card_name, card_discount_price, card_old_price, card_sale_date])

    async with aiofiles.open(f'{selected_store_names[shop_id]}_{cur_time}.csv', 'w', encoding='utf-8') as file:
        writer = AsyncWriter(file)

        await writer.writerow(
            [
                'Product',
                'New cost',
                'Old cost',
                # 'Discount (percent)',
                'Discount period',
            ]
        )
        await writer.writerows(data)

    return f'{selected_store_names[shop_id]}_{cur_time}.csv'


async def main():
    await collect_data(shop_id='7215')


if __name__ == '__main__':
    asyncio.run(main())
