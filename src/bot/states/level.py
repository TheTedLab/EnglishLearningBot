import telegram
from telegram import Update
from telegram.ext import CallbackContext

from src.bot.commands import unknown_response
from src.bot.constants import ACTION
from src.bot.logger import logger


# Класс функций и dispatcher состояний LEVEL_KNOWLEDGE и LEVEL_LANGUAGE
class LevelDispatch:
    def provide_teacher_func(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text(
            'Вам предоставлен преподаватель!'
        )

        return ACTION

    def link_func(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text(
            'Вот ссылка на тест: '
            '<a href="https://www.cambridgeenglish.org/test-your-english/general-english/">'
            'Cambridge Level Test</a>',
            parse_mode=telegram.ParseMode.HTML,
        )

        return ACTION

    def know_level_func(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text(
            'Хорошо. Тогда попробуйте другие функции!'
        )

        return ACTION

    def no_such_language(self, update: Update, context: CallbackContext) -> int:
        unknown_response(update, context)

        return ACTION

    def knowledge_dispatcher(self, choice, update, context):
        method = getattr(self, knowledge_switcher(choice))

        return method(update, context)

    def language_dispatcher(self, choice, update, context):
        method = getattr(self, language_switcher(choice))

        return method(update, context)


# Switch для LEVEL_KNOWLEDGE ответов
def knowledge_switcher(choice) -> str:
    switcher = {
        "Да": "provide_teacher_func",
        "Нет": "link_func"
    }

    return switcher.get(choice, "no_such_language")


# Switch для LEVEL_LANGUAGE ответов
def language_switcher(choice) -> str:
    switcher = {
        "Да": "link_func",
        "Нет": "know_level_func"
    }

    return switcher.get(choice, "no_such_language")


# Функция LEVEL_KNOWLEDGE состояния - знание об уровне после RECORD
def level_knowledge_func(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user.full_name
    text = update.message.text
    logger.info("<%s> knows English level: \"%s\"", user, text)
    # Вызов LEVEL_KNOWLEDGE dispatcher
    bot_knowledge_dispatch = LevelDispatch()

    return bot_knowledge_dispatch.knowledge_dispatcher(text, update, context)


# Функция LEVEL_LANGUAGE состояния - команда "Узнать уровень"
def level_language_func(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user.full_name
    text = update.message.text
    logger.info("<%s> want to know English level: \"%s\"", user, text)
    # Вызов LEVEL_LANGUAGE dispatcher
    bot_language_dispatch = LevelDispatch()

    return bot_language_dispatch.language_dispatcher(text, update, context)
