from config.botConfig import bot

UNKNOWN = "Неизвестно"


async def del_ques(message):
    message = message
    # await bot.delete_message(message.chat.id, User.user_data[message.chat.id][UserKeys.SCORE_MESS_ID])
    # await bot.delete_message(message.chat.id, User.user_data[message.chat.id][UserKeys.SCORE_MESS_ID] + 1)