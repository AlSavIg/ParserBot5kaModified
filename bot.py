from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiofiles import os
from stores import selected_stores
from my_parser import collect_data

token = "5387713157:AAHc0bfR2F8m1WzPiCfPa4_ACi0K39VCZV4"
bot = Bot(token=token)
dp = Dispatcher(bot)


def main():
    executor.start_polling(dp)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = [selected_stores.get(key) for key in selected_stores]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Пожалуйста, выберите магазин', reply_markup=keyboard)


async def send_data(shop_id, chat_id):
    file = await collect_data(shop_id=shop_id)
    await bot.send_document(chat_id=chat_id, document=open(file, 'rb'))
    await os.remove(file)


async def send_message(message, shop_id):
    await message.answer('Ожидайте...')
    chat_id = message.chat.id
    await send_data(shop_id=shop_id, chat_id=chat_id)


@dp.message_handler(Text(equals=selected_stores.get('5677')))
async def shop5677(message: types.Message):
    await send_message(message=message, shop_id='5677')


@dp.message_handler(Text(equals=selected_stores.get('33YU')))
async def shop33YU(message: types.Message):
    await send_message(message=message, shop_id='33YU')


@dp.message_handler(Text(equals=selected_stores.get('5593')))
async def shop5593(message: types.Message):
    await send_message(message=message, shop_id='5593')


@dp.message_handler(Text(equals=selected_stores.get('5415')))
async def shop5415(message: types.Message):
    await send_message(message=message, shop_id='5415')


@dp.message_handler(Text(equals=selected_stores.get('5600')))
async def shop5600(message: types.Message):
    await send_message(message=message, shop_id='5600')
            

@dp.message_handler(Text(equals=selected_stores.get('324M')))
async def shop324M(message: types.Message):
    await send_message(message=message, shop_id='324M')
            

@dp.message_handler(Text(equals=selected_stores.get('323W')))
async def shop323W(message: types.Message):
    await send_message(message=message, shop_id='323W')
