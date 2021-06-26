import random

import telegram
from telegram import Update
from telegram.ext import CallbackContext

from src.bot.commands import unknown_response
from src.bot.constants import right_triangle, ACTION, TIME_SIGN, LEVEL_KNOWLEDGE
from src.bot.logger import logger


# Класс функций и dispatcher состояний RECORD
class RecordFunctions:
    def teacher_sign_func(self, update: Update, context: CallbackContext) -> int:
        first_time = random_hour(6, 19)
        second_time = random_hour(7, 20)
        third_time = random_hour(8, 21)

        while second_time <= first_time:
            second_time = random_hour(7, 20)

        while third_time <= second_time:
            third_time = random_hour(8, 21)

        update.message.reply_text("На какое время? (Укажите номер)")
        update.message.reply_text(
            right_triangle + '1. *' + first_time + '*\n' +
            right_triangle + '2. *' + second_time + '*\n' +
            right_triangle + '3. *' + third_time + '*\n',
            parse_mode=telegram.ParseMode.MARKDOWN
        )
        context.user_data['1'] = first_time
        context.user_data['2'] = second_time
        context.user_data['3'] = third_time

        return TIME_SIGN

    def level_func(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("Знаете ли вы свой уровень английского языка?")

        return LEVEL_KNOWLEDGE

    def no_such_record(self, update: Update, context: CallbackContext) -> int:
        unknown_response(update, context)

        return ACTION

    def record_dispatcher(self, action, update, context):
        method = getattr(self, record_switcher(action))

        return method(update, context)


# Switch для RECORD ответов
def record_switcher(action) -> str:
    switcher = {
        "Да": "teacher_sign_func",
        "Нет": "level_func"
    }

    return switcher.get(action, "no_such_record")


# Функция RECORD состояния
def record_with_teacher(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user.full_name
    text = update.message.text
    logger.info("<%s> chose to record with teacher: \"%s\"", user, text)
    # Вызов RECORD dispatcher
    bot_record_functions = RecordFunctions()

    return bot_record_functions.record_dispatcher(text, update, context)


def random_hour(begin, end) -> str:
    str_hour = ""
    hour = random.randint(begin, end)
    if hour < 10:
        str_hour += "0"

    str_hour += str(hour) + ":00"

    return str_hour
