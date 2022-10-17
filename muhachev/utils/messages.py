from config.botConfig import bot
from productData import User, UserKeys


async def del_ques(message):
    await bot.delete_message(message.chat.id, User.user_data[message.chat.id][UserKeys.SCORE_MESS_ID])
    await bot.delete_message(message.chat.id, User.user_data[message.chat.id][UserKeys.SCORE_MESS_ID] + 1)