from telegram import Update
from telegram.ext import CallbackContext

from src.bot.commands import unknown_response
from src.bot.constants import ACTION, TEACHER_INFO
from src.bot.logger import logger


# Класс функций и dispatcher состояний TIME_SIGN
class TimeDispatch:
    def first_time(self, update: Update, context: CallbackContext) -> int:
        # Если запрос первого времени - очистка второго и третьего
        context.user_data['2'] = ""
        context.user_data['3'] = ""

        return TEACHER_INFO

    def second_time(self, update: Update, context: CallbackContext) -> int:
        # Если запрос второго времени - очистка первого и третьего
        context.user_data['1'] = ""
        context.user_data['3'] = ""

        return TEACHER_INFO

    def third_time(self, update: Update, context: CallbackContext) -> int:
        # Если запрос третьего времени - очистка первого и второго
        context.user_data['2'] = ""
        context.user_data['3'] = ""

        return TEACHER_INFO

    def no_such_time(self, update: Update, context: CallbackContext) -> int:
        unknown_response(update, context)

        return ACTION

    def time_dispatcher(self, time, update: Update, context: CallbackContext):
        method = getattr(self, time_switcher(time))

        return method(update, context)


# Switch для TIME_SIGN ответов
def time_switcher(time) -> str:
    switcher = {
        "1": "first_time",
        "2": "second_time",
        "3": "third_time"
    }

    return switcher.get(time, "no_such_time")


# Функция TIME_SIGN состояния - время записи к преподавателю
def teacher_time_func(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user.full_name
    text = update.message.text
    time = context.user_data[text]
    logger.info("<%s> chose time: \"%s\"", user, text)
    update.message.reply_text(
        fr'Вы успешно записались к преподавателю на время {time}!'
    )
    update.message.reply_text(
        "Вы хотите получить информацию о преподавателе?"
    )

    # Вызов TIME_SIGN dispatcher
    bot_time_dispatch = TimeDispatch()

    return bot_time_dispatch.time_dispatcher(text, update, context)
