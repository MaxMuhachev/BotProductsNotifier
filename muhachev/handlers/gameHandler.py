import random
from contextlib import suppress

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import MessageNotModified

from config.botConfig import dp, config, bot
from commands import Commands
from database.query import getQuestionBySection
from keyboards.keyboard import get_keyboard
from productData import User, UserKeys
from utils.messages import del_ques


async def cmd_start_game(message: types.Message):
    user_map_value = User.user_data.get(message.chat.id, 0)
    score_message = "Текущее количество очков: <b>"
    number_question = 1
    if user_map_value == 0:
        score_message += "0"
        User.user_data[message.chat.id] = {UserKeys.SCORE: 0,
                                           UserKeys.SECTION: 1,
                                           UserKeys.LAST_RESULT: "",
                                           UserKeys.CAN_HALF: True,
                                           UserKeys.CAN_ERROR: True,
                                           }
    else:
        await del_ques(message)
        number_question = User.user_data[message.chat.id][UserKeys.SECTION]
        score_message += str(User.user_data[message.chat.id][UserKeys.SCORE])

    score_message += "</b>"
    await message.answer(score_message,
                         parse_mode=types.ParseMode.HTML)
    User.user_data[message.chat.id][UserKeys.SCORE_MESS_ID] = message.message_id + 1
    questions = await getQuestionBySection(config, number_question)
    await message.answer(str(number_question) + ". " + questions[0][0] + "?",
                         reply_markup=get_keyboard(questions, message.chat.id))


@dp.callback_query_handler(Text(equals=Commands.HALF_ANSW))
async def cmd_half_ans(call: types.CallbackQuery):
    with suppress(MessageNotModified):
        User.user_data[call.message.chat.id][UserKeys.CAN_HALF] = False
        number_question = User.user_data[call.message.chat.id][UserKeys.SECTION]
        questions = await getQuestionBySection(config, number_question)
        while len(questions) != 2:
            i = random.randint(0, len(questions) - 1)
            if questions[i][3] != 1:
                questions.pop(i)
        await call.message.edit_text(str(number_question) + ". " + questions[0][0] + "?",
                                     reply_markup=get_keyboard(questions, call.message.chat.id))
        await call.answer()


@dp.callback_query_handler(Text(startswith="ans_"))
async def callbacks_game(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    # Парсим строку и извлекаем действие, например `ans_1` -> `ans_0`
    action = call.data.split("_")[1]
    if action == "1":
        User.user_data[chat_id][UserKeys.SCORE] += 1000 * User.user_data[chat_id][UserKeys.SECTION]
        User.user_data[chat_id][UserKeys.LAST_RESULT] = "верный!"
        await update_ques_text(call.message)
    else:
        User.user_data[chat_id][UserKeys.LAST_RESULT] = "не верный!"
        if User.user_data[chat_id][UserKeys.CAN_ERROR]:
            User.user_data[call.message.chat.id][UserKeys.CAN_ERROR] = False
            User.user_data[chat_id][UserKeys.LAST_RESULT] = "не верный! У вас не осталось права на ошибку."
            await update_ques_text(call.message)
        else:
            await call.message.delete()
            await cmd_cancel(call.message)
    # Не забываем отчитаться о получении колбэка
    await call.answer()


async def cmd_finish_game(message: types.Message):
    user_map_value = User.user_data.get(message.chat.id, 0)
    if user_map_value != 0:
        await del_ques(message)
        await message.answer("Последний ответ был <b>верный</b>\nСпасибо за игру. Вы заработали <b>" +
                             str(User.user_data[message.chat.id][UserKeys.SCORE]) + " очков</b>." +
                             "\nМы будем ждать тебя снова &#128151;",
                             parse_mode=types.ParseMode.HTML)
        User.user_data.pop(message.chat.id)
    else:
        await message.answer("Сначала начните игру &#128540;", parse_mode=types.ParseMode.HTML)


async def cmd_cancel(message: types.Message):
    await message.answer("Последний ответ был <b>" + User.user_data[message.chat.id][UserKeys.LAST_RESULT] +
                         "</b>\nСпасибо за игру. Вы набрали <b>" +
                         str(User.user_data[message.chat.id][UserKeys.SCORE]) + " очков</b>." +
                         "\nВ следующий раз вам повезёт больше &#128521;",
                         parse_mode=types.ParseMode.HTML)
    User.user_data.pop(message.chat.id)


async def update_ques_text(message: types.Message):
    with suppress(MessageNotModified):
        User.user_data[message.chat.id][UserKeys.SECTION] += 1

        await bot.edit_message_text(
            text="<b>Ответ " + User.user_data[message.chat.id][UserKeys.LAST_RESULT] +
                 "</b> Текущее количество очков: <b>" +
                 str(User.user_data[message.chat.id][UserKeys.SCORE]) + "</b>",
            chat_id=message.chat.id,
            message_id=User.user_data[message.chat.id][UserKeys.SCORE_MESS_ID],
            parse_mode=types.ParseMode.HTML)

        number_question = User.user_data[message.chat.id][UserKeys.SECTION]
        questions = await getQuestionBySection(config, number_question)
        if len(questions) > 0:
            await message.edit_text(str(number_question) + ". " + questions[0][0] + "?",
                                    reply_markup=get_keyboard(questions, message.chat.id))
        else:
            await cmd_finish_game(message)
