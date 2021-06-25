from telegram import Update
from telegram.ext import CallbackContext

from src.bot.commands import unknown_response
from src.bot.constants import ACTION
from src.bot.logger import logger


# Класс функций и dispatcher состояний TEACHER_INFO
class TeacherInfoDispatch:
    def teacher_about_func(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("Преподаватель!")

        return ACTION

    def no_about_func(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("Ок. Тогда попробуйте другие функции!")

        return ACTION

    def no_such_info(self, update: Update, context: CallbackContext) -> int:
        unknown_response(update, context)

        return ACTION

    def teacher_info_dispatcher(self, choice, update, context):
        method = getattr(self, teacher_info_switcher(choice))

        return method(update, context)


# Switch для TEACHER_INFO ответов
def teacher_info_switcher(choice) -> str:
    switcher = {
        "Да": "teacher_about_func",
        "Нет": "no_about_func"
    }

    return switcher.get(choice, "no_such_info")


# Функция TEACHER_INFO состояния - информация о преподавателе
def teacher_info_func(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user.full_name
    text = update.message.text
    logger.info("<%s> chose to get information about the teacher: %s", user, text)
    # Вызов TEACHER_INFO dispatcher
    bot_teacher_info = TeacherInfoDispatch()

    return bot_teacher_info.teacher_info_dispatcher(text, update, context)
