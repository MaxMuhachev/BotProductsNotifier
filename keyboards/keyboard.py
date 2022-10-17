from aiogram import types

from commands import Commands
from productData import ProductKeys


def get_keyboard(products):
    buttons = [types.InlineKeyboardButton(text=a[0], callback_data="not_" + str(a[1])) for a in products]
    # Генерация клавиатуры.
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_change_watch(products):
    buttons = [types.InlineKeyboardButton(text=a[0], callback_data="change_" + str(a[1])) for a in products]
    # Генерация клавиатуры.
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_stop_watch(products):
    buttons = [types.InlineKeyboardButton(text=a[0], callback_data="stop_" + str(a[1])) for a in products]
    # Генерация клавиатуры.
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard
