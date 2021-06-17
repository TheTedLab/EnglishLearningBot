import logging
import telegram

from authorization import token
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    MessageFilter,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

hand_emoji = u'\U0001F44B'
check_mark = u'\U00002705'
cross_mark = u'\U0000274C'
right_triangle = u'\U000025B6'

ACTION, RECORD_LEVEL_ONE, RECORD_LEVEL_TWO, TIME_SIGN, INFO, SERVICES, \
    LEVEL_KNOWLEDGE, LEVEL_LANGUAGE = range(8)


class FilterRecord(MessageFilter):
    def filter(self, message):
        return 'Запись на занятие' in message.text


class FilterInfo(MessageFilter):
    def filter(self, message):
        return 'Подробнее' in message.text


class FilterServices(MessageFilter):
    def filter(self, message):
        return 'Услуги' in message.text


class FilterLevel(MessageFilter):
    def filter(self, message):
        return 'Узнать уровень' in message.text


class FilterYes(MessageFilter):
    def filter(self, message):
        return 'Да' in message.text


class FilterNo(MessageFilter):
    def filter(self, message):
        return 'Нет' in message.text


filter_record = FilterRecord()
filter_info = FilterInfo()
filter_services = FilterServices()
filter_level = FilterLevel()
filter_yes = FilterYes()
filter_no = FilterNo()


def commands_text() -> str:
    return 'Что ты хочешь сделать?\n' \
           + check_mark + 'Напиши \"*Запись на занятие*\" - чтобы записаться на курсы к преподавателю\n' \
           + check_mark + 'Напиши \"*Подробнее*\" - чтобы получить дополнительную информацию о платформе\n' \
           + check_mark + 'Напиши \"*Услуги*\" - чтобы узнать об различных услугах платформы\n' \
           + check_mark + 'Напиши \"*Узнать уровень*\" - чтобы узнать свой уровень английского языка\n'


def commands_helper(update: Update, context: CallbackContext) -> None:
    unknown_response(update, context)
    update.message.reply_text(
        commands_text(),
        parse_mode=telegram.ParseMode.MARKDOWN
    )


def start(update: Update, context: CallbackContext) -> int:
    """Select an action: Record, Info, Services or Level."""
    user = update.effective_user
    logger.info("<%s> start conversation.", user.full_name)
    update.message.reply_text(
        hand_emoji + fr'Привет, {user.full_name}!' +
        '\n Я бот школы по изучению английского языка' +
        ' и я помогу тебе взаимодействовать с нашей платформой!\n' +
        commands_text(),
        parse_mode=telegram.ParseMode.MARKDOWN
    )

    return ACTION


class ActionFunctions:
    def record_func(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("Вы хотите записаться к конкретному преподавателю?")

        return RECORD_LEVEL_ONE

    def info_func(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text(
            fr'Школа английского языка. Бот: {context.bot.name} '
        )

        return ACTION

    def services_func(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text(
            "Услуги школы:\n" +
            right_triangle + "1. ОГЭ (ГИА)\n" +
            right_triangle + "2. ЕГЭ\n" +
            right_triangle + "3. IELTS (Любой экзамен)\n" +
            right_triangle + "4. Для себя\n"
        )

        return ACTION

    def level_func(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("Вы хотите узнать свой уровень английского языка?")

        return LEVEL_LANGUAGE

    def no_such_action(self, update: Update, context: CallbackContext) -> int:
        unknown_response(update, context)

        return ACTION

    def actions_dispatcher(self, action, update, context):
        method = getattr(self, actions_switcher(action))
        return method(update, context)


def actions_switcher(action) -> str:
    switcher = {
        "Запись на занятие": "record_func",
        "Подробнее": "info_func",
        "Услуги": "services_func",
        "Узнать уровень": "level_func"
    }

    return switcher.get(action, "no_such_action")


def action_func(update: Update, context: CallbackContext) -> str:
    user = update.message.from_user.full_name
    text = update.message.text
    logger.info("<%s> chose action: \"%s\"", user, text)
    # Call action function
    bot_action_functions = ActionFunctions()

    return bot_action_functions.actions_dispatcher(text, update, context)


class RecordFunctions:
    def teacher_sign_func(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("На какое время?")

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


def record_switcher(action) -> str:
    switcher = {
        "Да": "teacher_sign_func",
        "Нет": "level_func"
    }

    return switcher.get(action, "no_such_record")


def record_with_teacher(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user.full_name
    text = update.message.text
    logger.info("<%s> chose to record with teacher: \"%s\"", user, text)
    # Call second level record function
    bot_record_functions = RecordFunctions()

    return bot_record_functions.record_dispatcher(text, update, context)


def teacher_time_func(update: Update, context: CallbackContext) -> str:
    user = update.message.from_user.full_name
    text = update.message.text
    logger.info("<%s> chose time: \"%s\"", user, text)
    update.message.reply_text(
        fr'Вы успешно записались к преподавателю на время {text}!'
    )
    # Call teacher info function
    print('call teacher info function')

    return ACTION


class LevelDispatch:
    def provide_teacher_func(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text(
            'Вам предоставлен преподаватель!'
        )

        return ACTION

    def link_func(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text(
            'Вот ссылка на тест!'
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


def knowledge_switcher(choice):
    switcher = {
        "Да": "provide_teacher_func",
        "Нет": "link_func"
    }

    return switcher.get(choice, "no_such_language")


def language_switcher(choice):
    switcher = {
        "Да": "link_func",
        "Нет": "know_level_func"
    }

    return switcher.get(choice, "no_such_language")


def level_knowledge_func(update: Update, context: CallbackContext) -> str:
    user = update.message.from_user.full_name
    text = update.message.text
    logger.info("<%s> knows English level: \"%s\"", user, text)
    # Call language level dispatcher
    bot_knowledge_dispatch = LevelDispatch()

    return bot_knowledge_dispatch.knowledge_dispatcher(text, update, context)


def level_language_func(update: Update, context: CallbackContext) -> str:
    user = update.message.from_user.full_name
    text = update.message.text
    logger.info("<%s> want to know English level: \"%s\"", user, text)
    # Call language level dispatcher
    bot_language_dispatch = LevelDispatch()

    return bot_language_dispatch.language_dispatcher(text, update, context)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("<%s> canceled the conversation.", user.full_name)
    update.message.reply_text(
        'Ок! Разговор отменен.',
    )

    return ConversationHandler.END


def unknown_response(update: Update, context: CallbackContext) -> None:
    """Reply to an unknown command."""
    user = update.message.from_user.full_name
    text = update.message.text
    logger.info("<%s> entered unknown command: %s", user, text)
    update.message.reply_text(
        'Извините, я вас не понял.'
    )


def no_start_command(update: Update, context: CallbackContext) -> None:
    """Reply to write start command."""
    # Call unknown response, then send to start
    unknown_response(update, context)
    update.message.reply_text(
        'Чтобы начать разговор напишите /start.'
    )


def already_start_func(update: Update, context: CallbackContext) -> None:
    """Reply that the conversation has already started."""
    user = update.message.from_user.full_name
    logger.info("<%s> tried the command /start after beginning.", user)
    update.message.reply_text(
        'Вы уже начали разговор!'
    )


def unknown_response_yes_no(update: Update, context: CallbackContext) -> None:
    """Reply to write yes or no."""
    # Call unknown response, then send to yes or no
    unknown_response(update, context)
    update.message.reply_text(
        'Ответьте на вопрос \"*Да*\" ' + check_mark +
        ' или \"*Нет*\" ' + cross_mark,
        parse_mode=telegram.ParseMode.MARKDOWN
    )


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it with token
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ACTION: [
                MessageHandler(filter_record | filter_info | filter_services | filter_level,
                               action_func),
                MessageHandler(Filters.text & ~Filters.command &
                               ~filter_record & ~filter_info &
                               ~filter_services & ~filter_level &
                               ~filter_yes & ~filter_no, commands_helper),
                CommandHandler('start', already_start_func)
            ],
            RECORD_LEVEL_ONE: [
                MessageHandler(filter_yes | filter_no, record_with_teacher),
                MessageHandler(Filters.text & ~Filters.command &
                               ~filter_yes & ~filter_no, unknown_response_yes_no)
            ],
            TIME_SIGN: [MessageHandler(Filters.text, teacher_time_func)],
            LEVEL_KNOWLEDGE: [
                MessageHandler(filter_yes | filter_no, level_knowledge_func),
                MessageHandler(Filters.text & ~Filters.command &
                               ~filter_yes & ~filter_no, unknown_response_yes_no)
            ],
            LEVEL_LANGUAGE: [
                MessageHandler(filter_yes | filter_no, level_language_func),
                MessageHandler(Filters.text & ~Filters.command &
                               ~filter_yes & ~filter_no, unknown_response_yes_no)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command and control message - send unknown response on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, no_start_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until Ctrl-C pressed or the process receives stop.
    updater.idle()


if __name__ == '__main__':
    main()
