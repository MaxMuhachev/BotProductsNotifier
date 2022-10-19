#!venv/bin/python
import asyncio
import time

import schedule
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from commands import Commands
from config.botConfig import dp
from handlers.botHandler import cmd_start_watch, cmd_stop, cmd_change, scheduler_products_every_hour, \
    scheduler_products_low_price, scheduler_products_change_price, cmd_now_price
from handlers.mainHandler import cmd_start


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=Commands.START, state="*")


def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(cmd_now_price, Text(equals=Commands.NOW_PRICE), state="*")
    dp.register_message_handler(cmd_start_watch, Text(equals=Commands.START_WATCH), state="*")
    dp.register_message_handler(cmd_stop, Text(equals=Commands.STOP_WATCH), state="*")
    dp.register_message_handler(cmd_change, Text(equals=Commands.CHANGE_WATCH), state="*")


async def main():
    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_main(dp)
    asyncio.create_task(scheduler_products_every_hour())
    asyncio.create_task(scheduler_products_low_price())
    asyncio.create_task(scheduler_products_change_price())

    # Запуск поллинга
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
