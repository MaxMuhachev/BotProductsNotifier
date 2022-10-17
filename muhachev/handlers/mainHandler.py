from aiogram import types
from aiogram.dispatcher import FSMContext

from commands import Commands


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [Commands.START_GAME, Commands.FINISH_GAME]
    keyboard.add(*buttons)
    await message.answer(
        'Добро пожаловать в игру "Кто хочет стать миллионером. \nДля начала выберите <b>"Начать игру"</b>',
        parse_mode=types.ParseMode.HTML,
        reply_markup=keyboard
    )
