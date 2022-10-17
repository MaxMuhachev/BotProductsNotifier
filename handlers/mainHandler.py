from aiogram import types
from aiogram.dispatcher import FSMContext

from commands import Commands


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = [Commands.START_WATCH, Commands.STOP_WATCH, Commands.CHANGE_WATCH]
    keyboard.add(*buttons)
    await message.answer(
        'Добро пожаловать бот для отслеживания товара "ProductsNotification \nДля начала выберите <b>"Начать отслеживать товары"</b>',
        parse_mode=types.ParseMode.HTML,
        reply_markup=keyboard
    )
