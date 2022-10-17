#!venv/bin/python
import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from commands import Commands
from config.botConfig import dp
from handlers.gameHandler import cmd_start_game, cmd_finish_game
from handlers.mainHandler import cmd_start


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=Commands.START, state="*")


def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(cmd_start_game, Text(startswith=Commands.START_GAME), state="*")
    dp.register_message_handler(cmd_finish_game, Text(startswith=Commands.FINISH_GAME), state="*")


async def main():
    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_main(dp)

    # Запуск поллинга
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
