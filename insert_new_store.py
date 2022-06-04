def insert_new_store():
    shop_id_local = input('Print shop_id_local: ')
    local_name = input('Print address: ')
    with open('bot.py', 'a', encoding='utf-8') as bot_file:
        new_function = \
            f"""
@dp.message_handler(Text(equals=selected_stores.get('{shop_id_local}')))
async def shop{shop_id_local}(message: types.Message):
    await send_message(message=message, shop_id='{shop_id_local}')
            """
        bot_file.write('\n' + new_function)
    with open('stores.csv', 'a', encoding='utf-8') as stores_file:
        new_store = shop_id_local + ';' + local_name
        stores_file.write(new_store + '\n')


if __name__ == '__main__':
    insert_new_store()
