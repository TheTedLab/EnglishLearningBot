from telegram import Update
from telegram.ext import CallbackContext

from src.bot.commands import unknown_response, voice_yes_no
from src.bot.constants import ACTION, SERVICE_SELECTION
from src.bot.logger import logger


# Класс функций и dispatcher состояний SERVICES
class ServicesDispatch:
    def services_info(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("Какой? (Укажите номер или скажите голосом)")

        return SERVICE_SELECTION

    def no_about_services(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("Ок. Тогда попробуйте другие функции!")

        return ACTION

    def no_such_services(self, update: Update, context: CallbackContext) -> int:
        unknown_response(update, context)

        return ACTION

    def services_dispatcher(self, choice, update, context):
        method = getattr(self, services_switcher(choice))

        return method(update, context)


# Switch для SERVICES ответов
def services_switcher(choice) -> str:
    switcher = {
        "Да": "services_info",
        "Нет": "no_about_services"
    }

    return switcher.get(choice, "no_such_services")


# Функция SERVICES состояния
def services_func(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user.full_name
    text = update.message.text
    logger.info("<%s> chose to get services info: \"%s\"", user, text)
    # Вызов SERVICES dispatcher
    bot_services_info = ServicesDispatch()

    return bot_services_info.services_dispatcher(text, update, context)


# Обработка голосовых сообщений SERVICES состояния
def voice_services_yes_no(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user.full_name
    text = voice_yes_no(update, context)
    logger.info("<%s> chose to get services info: \"%s\" (voice)", user, text)
    # Вызов SERVICES dispatcher
    bot_services_info = ServicesDispatch()

    return bot_services_info.services_dispatcher(text, update, context)
