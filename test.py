import requests

items_on_page = 30
page = 1
shop_id = 5677
url = 'https://5ka.ru/api/v2/special_offers/' \
              f'?records_per_page={items_on_page}' \
              f'&page={page}' \
              f'&store={shop_id}' \
              '&ordering=' \
              '&price_promo__gte=' \
              '&price_promo__lte=' \
              '&categories=' \
              '&search='


def get_data():
    global url
    response = requests.get(url=url)
    data = response.json()
    while data.get('next') != 'null':
        url = data.get('next')
        results = data.get('results')
        for item in results:
            parsed_data = data_collector(item)
        response = requests.get(url=url)
        data = response.json()


def data_collector(item):
    name = item.get('name')
    img_link = item.get('img_link')
    promo_date_begin = item.get('promo').get('date_begin')
    promo_date_end = item.get('promo').get('date_end')
    old_price = item.get('current_prices').get('price_reg__min')
    new_price = item.get('current_prices').get('price_promo__min')
    discount = f'{(1 - new_price / old_price) * 100}%'
    return [name,
            img_link,
            promo_date_begin,
            promo_date_end,
            old_price,
            new_price,
            discount]


if __name__ == '__main__':
    pass
