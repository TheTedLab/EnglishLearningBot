import telegram
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from src.bot.constants import hand_emoji, check_mark, cross_mark, ACTION
from src.bot.logger import logger

from src.network.training.models.neural_models import model_gru_yn
from src.network.training.tokenizers.tokenizers import tokenizer_yn
from src.speech_recognition.speech_recognition import voice_processing, voice_pre_processing


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


def voice_yes_no_switcher(choice) -> str:
    switcher = {
        0: "Да",
        1: "Нет"
    }

    return switcher.get(choice, "Не понял")


# Запрос Да/Нет в любой подкатегории
def voice_yes_no(update: Update, context: CallbackContext) -> str:
    """Reply that received a yes/no voice message."""
    # Получаем пользователя
    user = update.message.from_user.full_name
    logger.info("<%s> was asked a question with yes or no answer.", user)

    # Отправляем на предобработку
    result_path = voice_pre_processing(update, context)

    # Отправляем на обработку в нейросеть
    text = voice_processing(result_path, tokenizer_yn, model_gru_yn, voice_yes_no_switcher)

    return text


# Любые запросы и команды внутри области без поддрежки голосовых
def voice_not_yet_support(update: Update, context: CallbackContext) -> None:
    """Reply to enter text."""
    # Вызов unknown_response, затем требование команды /start
    unknown_response(update, context)
    update.message.reply_text(
        'В этой области голосовые сообщения пока не поддерживаются.'
    )
    update.message.reply_text(
        'Попробуйте текстовые сообщения!'
    )
