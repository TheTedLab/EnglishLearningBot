from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

from authorization import token
from src.bot.commands import (
    start,
    commands_helper,
    already_start_func,
    help_conversation,
    unknown_response_yes_no,
    unknown_response_four_digit,
    unknown_response_three_digit,
    cancel,
    help_command,
    not_started_conversation,
    no_start_command,
    voice_not_yet_support
)
from src.bot.constants import (
    ACTION, RECORD, SERVICES, LEVEL_LANGUAGE, TIME_SIGN,
    LEVEL_KNOWLEDGE, SERVICE_SELECTION, TEACHER_INFO
)
from src.bot.filters import (
    filter_record, filter_services, filter_level, filter_info,
    filter_yes, filter_no,
    filter_digit_one, filter_digit_two, filter_digit_three, filter_digit_four
)
from src.bot.states.action import (
    action_func, action_voice_func
)
from src.bot.states.level import level_knowledge_func, level_language_func
from src.bot.states.record import record_with_teacher
from src.bot.states.service_selection import service_selection_func
from src.bot.states.services import services_func
from src.bot.states.teacher_info import teacher_info_func
from src.bot.states.time_sign import teacher_time_func


def main() -> None:
    """Start the bot."""
    # Создание Updater и связывание с токеном бота
    updater = Updater(token)

    # Получение dispatcher и регистрация handlers
    dispatcher = updater.dispatcher

    # Добавление conversation handler с состояниями разговора
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ACTION: [
                MessageHandler(Filters.voice, action_voice_func),
                MessageHandler(filter_record | filter_info | filter_services | filter_level,
                               action_func),
                MessageHandler(Filters.text & ~Filters.command |
                               filter_yes | filter_no, commands_helper),
                CommandHandler('start', already_start_func),
                CommandHandler('help', help_conversation)
            ],
            RECORD: [
                MessageHandler(Filters.voice, voice_not_yet_support),
                MessageHandler(filter_yes | filter_no, record_with_teacher),
                MessageHandler(Filters.text & ~Filters.command, unknown_response_yes_no),
                CommandHandler('start', already_start_func)
            ],
            SERVICES: [
                MessageHandler(Filters.voice, voice_not_yet_support),
                MessageHandler(filter_yes | filter_no, services_func),
                MessageHandler(Filters.text & ~Filters.command, unknown_response_yes_no),
                CommandHandler('start', already_start_func)
            ],
            SERVICE_SELECTION: [
                MessageHandler(Filters.voice, voice_not_yet_support),
                MessageHandler(filter_digit_one | filter_digit_two | filter_digit_three |
                               filter_digit_four, service_selection_func),
                MessageHandler(Filters.text & ~Filters.command, unknown_response_four_digit),
                CommandHandler('start', already_start_func)
            ],
            TIME_SIGN: [
                MessageHandler(Filters.voice, voice_not_yet_support),
                MessageHandler(filter_digit_one | filter_digit_two | filter_digit_three,
                               teacher_time_func),
                MessageHandler(Filters.text & ~Filters.command, unknown_response_three_digit),
                CommandHandler('start', already_start_func)
            ],
            LEVEL_KNOWLEDGE: [
                MessageHandler(Filters.voice, voice_not_yet_support),
                MessageHandler(filter_yes | filter_no, level_knowledge_func),
                MessageHandler(Filters.text & ~Filters.command, unknown_response_yes_no),
                CommandHandler('start', already_start_func)
            ],
            LEVEL_LANGUAGE: [
                MessageHandler(Filters.voice, voice_not_yet_support),
                MessageHandler(filter_yes | filter_no, level_language_func),
                MessageHandler(Filters.text & ~Filters.command, unknown_response_yes_no),
                CommandHandler('start', already_start_func)
            ],
            TEACHER_INFO: [
                MessageHandler(Filters.voice, voice_not_yet_support),
                MessageHandler(filter_yes | filter_no, teacher_info_func),
                MessageHandler(Filters.text & ~Filters.command, unknown_response_yes_no),
                CommandHandler('start', already_start_func)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Регистрация команд - ответы в Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("cancel", not_started_conversation))

    # Любые сообщения и команды до начала разговора - ответ нет /start команды
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, no_start_command))

    # Голосовое сообщение до начала разговора
    dispatcher.add_handler(MessageHandler(Filters.voice, no_start_command))

    # Старт бота
    updater.start_polling()

    # Бот работает до прерывания Ctrl-C или получения stop команды
    updater.idle()


if __name__ == '__main__':
    main()
