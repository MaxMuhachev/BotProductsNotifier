import asyncio
import json
import string
from urllib.parse import quote

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from commands import Commands
from config.botConfig import dp, config, bot
from database.query import get_product_py_name, add_product, add_watch_product, \
    find_notif_every_hours, update_last_notification_time, update_chat_every_hour, \
    get_last_product_id_by_chat_id, update_low_price, find_notif_low_price, get_products_by_chat_id, \
    update_date_updated, get_product_py_id, delete_user_track, update_prod_notif_change, find_notif_change_price, \
    get_product_last_price, update_last_price, find_notif_for_update_price
from keyboards.keyboard import get_keyboard, get_keyboard_change_watch, get_keyboard_stop_watch
from parse.parseStore import get_html
from productData import ProductKeys, StoreFields, CONFIG_STORE_FILE
from utils.messages import UNKNOWN


class Products(StatesGroup):
    product_name = State()
    product_name_price_now = State()
    after_hours = State()
    low_price = State()


async def cmd_start_watch(message: types.Message):
    await message.answer("Введите <b>название</b> товара, который хотите отслеживать", parse_mode=types.ParseMode.HTML)
    await Products.product_name.set()


async def cmd_now_price(message: types.Message):
    await message.answer("Введите <b>название</b> товара цены которого хотите получить", parse_mode=types.ParseMode.HTML)
    await Products.product_name_price_now.set()


async def cmd_change(message: types.Message):
    products = await get_products_by_chat_id(config, message.chat.id)
    if len(products):
        await message.answer("<b>Выберите товар</b> для изменения",
                             reply_markup=get_keyboard_change_watch(products),
                             parse_mode=types.ParseMode.HTML)
    else:
        await message.answer("Сейчас нет отслеживаемых товаров",
                             parse_mode=types.ParseMode.HTML)


async def cmd_stop(message: types.Message):
    products = await get_products_by_chat_id(config, message.chat.id)
    if len(products):
        await message.answer("<b>Выберите товар</b> для того, чтобы перестать отслеживать",
                             reply_markup=get_keyboard_stop_watch(products),
                             parse_mode=types.ParseMode.HTML)
    else:
        await message.answer("Сейчас нет отслеживаемых товаров",
                             parse_mode=types.ParseMode.HTML)


@dp.message_handler(state=Products.product_name)
async def set_product_name(message: types.Message, state: FSMContext):
    productMessage = message.text.lower().translate(str.maketrans('', '', string.punctuation))
    productDb = await get_product_py_name(config, productMessage)
    if productDb is None:
        productDb = add_product(config, productMessage)
    update_date_updated(config, productDb[0])

    await add_watch_product(config, message.chat.id, productDb[0])
    await message.answer("Выберите вариант оповещения уведомлениями",
                         reply_markup=get_keyboard([[Commands.EVERY_HOUR_PRICE, ProductKeys.EVERY],
                                                    [Commands.CHANGE_PRICE, ProductKeys.CHANGE],
                                                    [Commands.LOW_PRICE, ProductKeys.LOW]]))
    await state.finish()


@dp.message_handler(state=Products.product_name_price_now)
async def set_product_name(message: types.Message, state: FSMContext):
    productMessage = message.text.lower().translate(str.maketrans('', '', string.punctuation))
    productDb = await get_product_py_name(config, productMessage)
    if productDb is None:
        productDb = add_product(config, productMessage)
    update_date_updated(config, productDb[0])
    mess = await get_product_prices_now([{0: str(message.chat.id), 1: str(productDb[0]), 2: productDb[1]}])

    await message.answer(
        "Текущие цены в магазинах: \n\n" + mess,
        parse_mode=types.ParseMode.HTML)
    await state.finish()


@dp.message_handler(state=Products.after_hours)
async def set_notif_every_hour(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        last_product_id = await get_last_product_id_by_chat_id(config, message.chat.id)
        await update_chat_every_hour(
            config,
            message.chat.id,
            last_product_id[0],
            message.text
        )
        await state.finish()
        await message.answer("Спасибо, мы будем присылать Вам уведомления каждые " + message.text + " ч.",
                             parse_mode=types.ParseMode.HTML)
        name_product = await get_product_py_id(config, last_product_id[0])
        mess = await get_product_prices_now([{0: str(message.chat.id), 1: str(last_product_id[0]), 2: name_product[0]}])
        await message.answer(
            "Текущие цены в магазинах: \n\n" + mess,
            parse_mode=types.ParseMode.HTML)
    else:
        await message.answer("<b>Колличество часов не является числом. Введите заново.</b>",
                             parse_mode=types.ParseMode.HTML)
        await state.finish()
        await Products.after_hours.set()


@dp.message_handler(state=Products.low_price)
async def set_notif_low_price(message: types.Message, state: FSMContext):
    while not message.text.isdigit():
        await message.answer("<b>Цена не является числом. Введите заново.</b>",
                             parse_mode=types.ParseMode.HTML)
        await state.finish()
        await Products.low_price.set()
    last_product_id = await get_last_product_id_by_chat_id(config, message.chat.id)
    await update_low_price(
        config,
        message.chat.id,
        last_product_id[0],
        message.text
    )
    await state.finish()
    await message.answer("Спасибо, мы пришлём Вам уведомление когда цена станет ниже " + message.text + " руб.",
                         parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(Text(startswith="not_"))
async def callbacks_watch_main_menu(call: types.CallbackQuery):
    # Парсим строку и извлекаем действие, например `not_1` -> `not_0`
    action = call.data.split("_")[1]
    if action == ProductKeys.EVERY:
        await call.message.answer("Введите через сколько <b>часов</b> вы хотите получать уведомления",
                                  parse_mode=types.ParseMode.HTML)
        await Products.after_hours.set()
    if action == ProductKeys.CHANGE:
        await change_price_notification_set(call)
    if action == ProductKeys.LOW:
        await call.message.answer("Введите <b>цену</b>.\nКогда товар будет по этой цене, мы пришлём уведомление.",
                                  parse_mode=types.ParseMode.HTML)
        await Products.low_price.set()
    await call.answer()


async def change_price_notification_set(call):
    last_product_id = await get_last_product_id_by_chat_id(config, call.message.chat.id)
    await update_prod_notif_change(config, call.message.chat.id, last_product_id[0])

    notif_change_price = await find_notif_for_update_price(config, call.message.chat.id, last_product_id[0])
    message = await get_product_prices_now(notif_change_price, True)

    await call.message.answer(
        "Спасибо, мы будем присылать Вам уведомления как только цена изменится. \n\nТекущие цены: \n" + message,
        parse_mode=types.ParseMode.HTML)


async def get_product_prices_now(notif_change_price, change_price=False):
    for notification in notif_change_price:
        with open(CONFIG_STORE_FILE, "r") as read_file:
            data_json = json.load(read_file)
            message = ""
            for data in data_json:
                message += "<b>Товар в магазине "
                data[StoreFields.URL] += quote(notification[2])
                data_store = get_html(data, notification[2])
                message = await create_store_message(data, data_store, message)
                if change_price and len(data_store.price) > 0:
                    await update_last_price(config, notification[1], data[StoreFields.STORE], data_store.price)
    return message


@dp.callback_query_handler(Text(startswith="change_"))
async def callbacks_change_notif(call: types.CallbackQuery):
    # Парсим строку и извлекаем действие, например `not_1` -> `not_0`
    product_id = call.data.split("_")[1]
    product_name = await get_product_py_id(config, product_id)
    await call.message.answer("Вы выбрали товар <b>" + product_name[0] + "</b>",
                              parse_mode=types.ParseMode.HTML)

    update_date_updated(config, product_id)
    await call.message.answer("Выберите вариант оповещения уведомлениями",
                              reply_markup=get_keyboard([[Commands.EVERY_HOUR_PRICE, ProductKeys.EVERY],
                                                         [Commands.CHANGE_PRICE, ProductKeys.CHANGE],
                                                         [Commands.LOW_PRICE, ProductKeys.LOW]]))
    await call.answer()


@dp.callback_query_handler(Text(startswith="stop_"))
async def callbacks_stop(call: types.CallbackQuery):
    # Парсим строку и извлекаем действие, например `not_1` -> `not_0`
    product_id = call.data.split("_")[1]
    product_name = await get_product_py_id(config, product_id)
    await call.message.answer("Вы перестали ослеживать товар <b>" + product_name[0] + "</b>",
                              parse_mode=types.ParseMode.HTML)
    await delete_user_track(config, call.message.chat.id, product_id)
    await call.answer()


async def scheduler_products_every_hour():
    while True:
        notif_every_hours = await find_notif_every_hours(config)

        for notification in notif_every_hours:
            with open(CONFIG_STORE_FILE, "r") as read_file:
                data_json = json.load(read_file)
                message = ""
                for data in data_json:
                    message += "<b>Товар в магазине "
                    data[StoreFields.URL] +=  quote(notification[2])
                    data_store = get_html(data, notification[2])
                    message = await create_store_message(data, data_store, message)

            await bot.send_message(text=message,
                                   chat_id=notification[0],
                                   parse_mode=types.ParseMode.HTML)
            await update_last_notification_time(config, notification[0], notification[1])
        await asyncio.sleep(int(config['Message']['timeout']))


async def scheduler_products_low_price():
    while True:
        notif_low_price = await find_notif_low_price(config)

        for notification in notif_low_price:
            with open(CONFIG_STORE_FILE, "r") as read_file:
                data_json = json.load(read_file)
                message = ""
                for data in data_json:
                    message += "<b>Товар НИЖЕ вашей цены в магазине "
                    data[StoreFields.URL] +=  quote(notification[2])
                    data_store = get_html(data, notification[2])
                    if len(data_store.price) and int(data_store.price) < int(notification[3]):
                        message = await create_store_message(data, data_store, message)
                        await bot.send_message(text=message,
                                               chat_id=notification[0],
                                               reply_markup=get_keyboard(
                                                   [[Commands.EVERY_HOUR_PRICE, ProductKeys.EVERY],
                                                    [Commands.CHANGE_PRICE, ProductKeys.CHANGE],
                                                    [Commands.LOW_PRICE, ProductKeys.LOW]]),
                                               parse_mode=types.ParseMode.HTML)

        await asyncio.sleep(int(config['Message']['timeout']))


async def scheduler_products_change_price():
    while True:
        notif_change_price = await find_notif_change_price(config)

        for notification in notif_change_price:
            with open(CONFIG_STORE_FILE, "r") as read_file:
                data_json = json.load(read_file)
                message = ""
                for data in data_json:
                    message += "<b>Цена на товар изменилась в магазине "
                    data[StoreFields.URL] +=  quote(notification[2])
                    data_store = get_html(data, notification[2])
                    last_price = await get_product_last_price(config, notification[0], notification[1],
                                                              data[StoreFields.STORE])
                    if len(data_store.price) and last_price[0] is not None and int(data_store.price) != int(last_price[0]):
                        message = await create_store_message(data, data_store, message)
                        message += "\n <b>Старая цена " + last_price[0] + " руб.</b>"
                        await bot.send_message(text=message,
                                               chat_id=notification[0],
                                               reply_markup=get_keyboard(
                                                   [[Commands.EVERY_HOUR_PRICE, ProductKeys.EVERY],
                                                    [Commands.CHANGE_PRICE, ProductKeys.CHANGE],
                                                    [Commands.LOW_PRICE, ProductKeys.LOW]]),
                                               parse_mode=types.ParseMode.HTML)

        await asyncio.sleep(int(config['Message']['timeout_change_price']))


async def create_store_message(data, data_store, message):
    message += data[StoreFields.STORE] + "</b>: "
    if data_store.product_not_found():
        message += "Не найден"
    else:
        if data_store.name is None:
            message += UNKNOWN
        else:
            if len(data_store.price) == 0:
                message += "Нет в наличии"
            else:
                message += data_store.name
                message += "\n<b>Цена: </b>" + data_store.price
                message += "\n<b>Ссылка: </b>" + data_store.link_url
    message += "\n\n"
    return message
