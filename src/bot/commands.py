from pathlib import Path

import telegram
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from src.bot.constants import hand_emoji, check_mark, cross_mark, ACTION
from src.bot.logger import logger
from src.conversion.opusToWav import opus_to_wav


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
    file = context.bot.getFile(voice.file_id)

    # Директория корневого каталога
    dir_path = Path.cwd().parent

    # Директории источника и результата
    source_path = Path(dir_path, 'conversion', 'oggFiles', 'voice.ogg')
    result_path = Path(dir_path, 'conversion', 'wavFiles', 'voice.wav')
    # Скачиваем голосовой файл и помещаем в oggFiles
    file.download(custom_path=source_path)
    # Берем из oggFiles и конвертируем в wav, помещая в wavFiles
    opus_to_wav(str(source_path), str(result_path))
    # Открываем wav-файл и отправляем для проверки
    with open(result_path, 'rb') as output:
        wav_file = output.read()
    update.message.reply_audio(wav_file, title='voice.wav')
