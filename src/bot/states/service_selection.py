import telegram

from telegram import Update
from telegram.ext import CallbackContext

from src.bot.logger import logger
from src.bot.commands import unknown_response
from src.bot.constants import ACTION, RECORD


# Класс функций и dispatcher состояний SERVICE_SELECTION
class ServiceSelection:
    def first_service(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text(
            'Вы выбрали услугу подготовки к *ОГЭ (ГИА)*.',
            parse_mode=telegram.ParseMode.MARKDOWN
        )

        return service_action_question(update, context)

    def second_service(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text(
            'Вы выбрали услугу подготовки к *ЕГЭ*.',
            parse_mode=telegram.ParseMode.MARKDOWN
        )

        return service_action_question(update, context)

    def third_service(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text(
            'Вы выбрали услугу подготовки к *IELTS (Любой экзамен)*.',
            parse_mode=telegram.ParseMode.MARKDOWN
        )

        return service_action_question(update, context)

    def fourth_service(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text(
            'Вы выбрали услугу подготовки \"*Для себя*\".',
            parse_mode=telegram.ParseMode.MARKDOWN
        )

        return service_action_question(update, context)

    def no_such_selection(self, update: Update, context: CallbackContext) -> int:
        unknown_response(update, context)

        return ACTION

    def selection_dispatcher(self, choice, update: Update, context: CallbackContext):
        method = getattr(self, service_selection_switcher(choice))

        return method(update, context)


# Switch для SERVICE_SELECTION ответов
def service_selection_switcher(choice) -> str:
    switcher = {
        "1": "first_service",
        "2": "second_service",
        "3": "third_service",
        "4": "fourth_service"
    }

    return switcher.get(choice, "no_such_selection")


# Функция SERVICE_SELECTION состояния
def service_selection_func(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user.full_name
    text = update.message.text
    logger.info("<%s> chose to get %s service.", user, text)
    # Вызов SERVICE_SELECTION dispatcher
    bot_selection_service = ServiceSelection()

    return bot_selection_service.selection_dispatcher(text, update, context)


# Вопрос о записи к преподавателю
def service_action_question(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Вы хотите записаться к конкретному преподавателю?'
    )

    return RECORD
