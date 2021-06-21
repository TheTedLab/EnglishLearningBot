import logging
import random

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

# Логирование в консоль
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# UTF-8 коды для эмодзи
hand_emoji = u'\U0001F44B'
check_mark = u'\U00002705'
cross_mark = u'\U0000274C'
right_triangle = u'\U000025B6'

# Перечисление состояний разговора
ACTION, RECORD, TIME_SIGN, INFO, SERVICES, SERVICE_SELECTION, LEVEL_KNOWLEDGE, \
    LEVEL_LANGUAGE, TEACHER_INFO = range(9)


# Фильтры текста
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


class FilterDigitOne(MessageFilter):
    def filter(self, message):
        return '1' in message.text


class FilterDigitTwo(MessageFilter):
    def filter(self, message):
        return '2' in message.text


class FilterDigitThree(MessageFilter):
    def filter(self, message):
        return '3' in message.text


class FilterDigitFour(MessageFilter):
    def filter(self, message):
        return '4' in message.text


filter_record = FilterRecord()
filter_info = FilterInfo()
filter_services = FilterServices()
filter_level = FilterLevel()
filter_yes = FilterYes()
filter_no = FilterNo()
filter_digit_one = FilterDigitOne()
filter_digit_two = FilterDigitTwo()
filter_digit_three = FilterDigitThree()
filter_digit_four = FilterDigitFour()


# Функция стандартного текста команд
def commands_text() -> str:
    return 'Что ты хочешь сделать?\n' \
           + check_mark + 'Напиши \"*Запись на занятие*\" - чтобы записаться на курсы к преподавателю\n' \
           + check_mark + 'Напиши \"*Подробнее*\" - чтобы получить дополнительную информацию о платформе\n' \
           + check_mark + 'Напиши \"*Услуги*\" - чтобы узнать об различных услугах платформы\n' \
           + check_mark + 'Напиши \"*Узнать уровень*\" - чтобы узнать свой уровень английского языка\n'


# Функция вывода текста команд
def commands_helper(update: Update, context: CallbackContext) -> None:
    unknown_response(update, context)
    update.message.reply_text(
        commands_text(),
        parse_mode=telegram.ParseMode.MARKDOWN
    )


# Стартовая функция - команда /start
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


# Класс функций и dispatcher состояний ACTION
class ActionFunctions:
    def record_func(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("Вы хотите записаться к конкретному преподавателю?")

        return RECORD

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
        update.message.reply_text(
            'Вы хотите воспользоваться какой-либо услугой?'
        )

        return SERVICES

    def level_func(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("Вы хотите узнать свой уровень английского языка?")

        return LEVEL_LANGUAGE

    def no_such_action(self, update: Update, context: CallbackContext) -> int:
        unknown_response(update, context)

        return ACTION

    def actions_dispatcher(self, action, update, context):
        method = getattr(self, actions_switcher(action))
        return method(update, context)


# Switch для ACTION ответов
def actions_switcher(action) -> str:
    switcher = {
        "Запись на занятие": "record_func",
        "Подробнее": "info_func",
        "Услуги": "services_func",
        "Узнать уровень": "level_func"
    }

    return switcher.get(action, "no_such_action")


# Функция ACTION состояния
def action_func(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user.full_name
    text = update.message.text
    logger.info("<%s> chose action: \"%s\"", user, text)
    # Вызов ACTION dispatcher
    bot_action_functions = ActionFunctions()

    return bot_action_functions.actions_dispatcher(text, update, context)


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


# Класс функций и dispatcher состояний SERVICES
class ServicesDispatch:
    def services_info(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("Какой? (Укажите номер)")

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


# Команда /help
def help_conversation(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued in conversation."""
    user = update.message.from_user.full_name
    logger.info("<%s> requested /help command in conversation.", user)
    update.message.reply_text('Помощь:')
    update.message.reply_text(
        commands_text(),
        parse_mode=telegram.ParseMode.MARKDOWN
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when command /help is issued."""
    user = update.message.from_user.full_name
    logger.info("<%s> requested /help command.", user)
    update.message.reply_text('Помощь:')
    update.message.reply_text(
        '*/start* - начать разговор;\n'
        '*/cancel* - закончить разговор;\n'
        '*/help* - помощь.\n',
        parse_mode=telegram.ParseMode.MARKDOWN
    )


# Команда отмены разговора
def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user.full_name
    logger.info("<%s> canceled the conversation.", user)
    update.message.reply_text(
        'Ок! Разговор отменен.',
    )

    return ConversationHandler.END


# Неизвестный запрос или команда
def unknown_response(update: Update, context: CallbackContext) -> None:
    """Reply to an unknown command."""
    user = update.message.from_user.full_name
    text = update.message.text
    logger.info("<%s> entered unknown command: %s", user, text)
    update.message.reply_text(
        'Извините, команда не распознана.'
    )


# Любые запросы и команды до начала разговора /start
def no_start_command(update: Update, context: CallbackContext) -> None:
    """Reply to enter start command."""
    # Вызов unknown_response, затем требование команды /start
    unknown_response(update, context)
    update.message.reply_text(
        'Чтобы начать разговор напишите /start.'
    )


# Повторные вызовы /start после начала разговора
def already_start_func(update: Update, context: CallbackContext) -> None:
    """Reply that the conversation has already started."""
    user = update.message.from_user.full_name
    logger.info("<%s> tried the command /start after beginning.", user)
    update.message.reply_text(
        'Вы уже начали разговор!'
    )


# Вызов /cancel до начала разговора
def not_started_conversation(update: Update, context: CallbackContext) -> None:
    """Reply that the conversation has not started yet."""
    user = update.message.from_user.full_name
    logger.info("<%s> tried the command /cancel before beginning.", user)
    update.message.reply_text(
        'Разговор еще не начат!'
    )
    update.message.reply_text(
        'Чтобы начать разговор напишите /start.'
    )


# Неизвестный запрос или команда при вопросе "Да или Нет"
def unknown_response_yes_no(update: Update, context: CallbackContext) -> None:
    """Reply to enter yes or no."""
    # Вызов unknown_response, затем требование "Да или Нет"
    unknown_response(update, context)
    update.message.reply_text(
        'Ответьте на вопрос \"*Да*\" ' + check_mark +
        ' или \"*Нет*\" ' + cross_mark,
        parse_mode=telegram.ParseMode.MARKDOWN
    )


# Неизвестный запрос или команда при вопросе с цифрами
def unknown_response_three_digit(update: Update, context: CallbackContext) -> None:
    """Reply to enter digit"""
    # Вызов unknown_response, затем требование цифры
    unknown_response(update, context)
    update.message.reply_text(
        'Ответьте на вопрос \'*1*\', \'*2*\' или \'*3*\'',
        parse_mode=telegram.ParseMode.MARKDOWN
    )


# Неизвестный запрос или команда при вопросе с цифрами
def unknown_response_four_digit(update: Update, context: CallbackContext) -> None:
    """Reply to enter digit"""
    # Вызов unknown_response, затем требование цифры
    unknown_response(update, context)
    update.message.reply_text(
        'Ответьте на вопрос \'*1*\', \'*2*\', \'*3*\' или \'*4*\'',
        parse_mode=telegram.ParseMode.MARKDOWN
    )


# Обработка голосовых сообщений - Доработка:
# 1. Посылает в голосовой преобразователь -> Далее в нейросеть
# 2. Принимает из нейросети -> Прогон по фильтрам
# 3. Возвращает боту
def voice_func(update: Update, context: CallbackContext) -> None:
    """Reply that received a voice message."""
    user = update.message.from_user.full_name
    voice = update.message.voice
    logger.info("<%s> entered voice message. Duration: %s, Size: %s",
                user, voice.duration, voice.file_size)
    update.message.reply_text(
        "Вы ввели голосовое сообщение.\nПоддержка голосовых сообщений в разработке..."
    )
    print('Get voice message')


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
                MessageHandler(Filters.voice, voice_func),
                MessageHandler(filter_record | filter_info | filter_services | filter_level,
                               action_func),
                MessageHandler(Filters.text & ~Filters.command |
                               filter_yes | filter_no, commands_helper),
                CommandHandler('start', already_start_func),
                CommandHandler('help', help_conversation)
            ],
            RECORD: [
                MessageHandler(Filters.voice, voice_func),
                MessageHandler(filter_yes | filter_no, record_with_teacher),
                MessageHandler(Filters.text & ~Filters.command, unknown_response_yes_no),
                CommandHandler('start', already_start_func)
            ],
            SERVICES: [
                MessageHandler(Filters.voice, voice_func),
                MessageHandler(filter_yes | filter_no, services_func),
                MessageHandler(Filters.text & ~Filters.command, unknown_response_yes_no),
                CommandHandler('start', already_start_func)
            ],
            SERVICE_SELECTION: [
                MessageHandler(Filters.voice, voice_func),
                MessageHandler(filter_digit_one | filter_digit_two | filter_digit_three |
                               filter_digit_four, service_selection_func),
                MessageHandler(Filters.text & ~Filters.command, unknown_response_four_digit),
                CommandHandler('start', already_start_func)
            ],
            TIME_SIGN: [
                MessageHandler(Filters.voice, voice_func),
                MessageHandler(filter_digit_one | filter_digit_two | filter_digit_three,
                               teacher_time_func),
                MessageHandler(Filters.text & ~Filters.command, unknown_response_three_digit),
                CommandHandler('start', already_start_func)
            ],
            LEVEL_KNOWLEDGE: [
                MessageHandler(Filters.voice, voice_func),
                MessageHandler(filter_yes | filter_no, level_knowledge_func),
                MessageHandler(Filters.text & ~Filters.command, unknown_response_yes_no),
                CommandHandler('start', already_start_func)
            ],
            LEVEL_LANGUAGE: [
                MessageHandler(Filters.voice, voice_func),
                MessageHandler(filter_yes | filter_no, level_language_func),
                MessageHandler(Filters.text & ~Filters.command, unknown_response_yes_no),
                CommandHandler('start', already_start_func)
            ],
            TEACHER_INFO: [
                MessageHandler(Filters.voice, voice_func),
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
    dispatcher.add_handler(MessageHandler(Filters.voice, voice_func))

    # Старт бота
    updater.start_polling()

    # Бот работает до прерывания Ctrl-C или получения stop команды
    updater.idle()


if __name__ == '__main__':
    main()
