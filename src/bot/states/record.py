import random

from telegram import Update
from telegram.ext import CallbackContext

from src.bot.commands import unknown_response, voice_yes_no
from src.bot.constants import ACTION, TIME_SIGN, LEVEL_KNOWLEDGE
from src.bot.logger import logger


# Класс функций и dispatcher состояний RECORD
class RecordFunctions:
    def teacher_sign_func(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("На какое время?")
        update.message.reply_text('Укажите любой час с 9:00 до 17:00.')

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


# Генерация рандомного часа
def random_hour(begin, end) -> str:
    """Generates random hour from begin time to end"""
    str_hour = ""
    hour = random.randint(begin, end)
    if hour < 10:
        str_hour += "0"

    str_hour += str(hour) + ":00"

    return str_hour


# Обработка голосовых сообщений RECORD состояния
def voice_record_yes_no(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user.full_name
    text = voice_yes_no(update, context)
    logger.info("<%s> chose to record with teacher: \"%s\" (voice)", user, text)
    # Вызов RECORD dispatcher
    bot_record_functions = RecordFunctions()

    return bot_record_functions.record_dispatcher(text, update, context)
