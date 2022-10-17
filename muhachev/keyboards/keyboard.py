from aiogram import types

from productData import User, UserKeys


def get_keyboard(answers, chat_id):
    buttons = [types.InlineKeyboardButton(text=a[2], callback_data="ans_" + str(a[3])) for a in answers]
    if User.user_data[chat_id][UserKeys.CAN_HALF]:
        buttons.append(types.InlineKeyboardButton(text="50/50", callback_data="half"))
    # Генерация клавиатуры.
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard