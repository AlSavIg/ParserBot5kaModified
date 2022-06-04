selected_stores = dict()

with open('stores.csv', 'r', encoding='utf-8') as file:
    for line in file:
        shop_id, name = map(str, line.split(';'))
        selected_stores[shop_id] = name.replace('\n', '')
