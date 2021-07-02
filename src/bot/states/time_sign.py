from telegram import Update
from telegram.ext import CallbackContext

from src.bot.constants import TEACHER_INFO
from src.bot.logger import logger
from src.network.training.models.neural_models import model_gru_times
from src.network.training.tokenizers.tokenizers import tokenizer_times
from src.speech_recognition.speech_recognition import voice_pre_processing, voice_processing


# Функция TIME_SIGN состояния - время записи к преподавателю
def teacher_time_func(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user.full_name
    text = update.message.text
    logger.info("<%s> chose time: \"%s\"", user, text)
    update.message.reply_text(
        fr'Вы успешно записались к преподавателю на время {text}!'
    )
    update.message.reply_text(
        "Вы хотите получить информацию о преподавателе?"
    )

    return TEACHER_INFO


# Switch для TIME_SIGN ответов нейросети
def voice_time_sign_switcher(choice) -> str:
    switcher = {
        0: "9:00",
        1: "10:00",
        2: "11:00",
        3: "12:00",
        4: "13:00",
        5: "14:00",
        6: "15:00",
        7: "16:00",
        8: "17:00",
        9: "18:00"
    }

    return switcher.get(choice, "no_such_time")


# Обработка голосовых сообщений TIME_SIGN состояния
def voice_time_sign(update: Update, context: CallbackContext) -> int:
    # Получаем пользователя
    user = update.message.from_user.full_name

    # Отправляем на предобработку
    result_path = voice_pre_processing(update, context)

    # Отправляем на обработку в нейросеть
    text = voice_processing(result_path, tokenizer_times, model_gru_times, voice_time_sign_switcher)

    # Логирование
    logger.info("<%s> chose time: \"%s\"", user, text)

    update.message.reply_text(
        fr'Вы успешно записались к преподавателю на время {text}!'
    )
    update.message.reply_text(
        "Вы хотите получить информацию о преподавателе?"
    )

    return TEACHER_INFO
