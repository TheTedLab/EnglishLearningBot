from pathlib import Path
from telegram import Update
from telegram.ext import CallbackContext

from src.bot.commands import unknown_response
from src.bot.constants import right_triangle, ACTION, RECORD, SERVICES, LEVEL_LANGUAGE
from src.bot.logger import logger

from src.conversion.opusToWav import opus_to_wav

import requests
import json
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow.keras.models
import numpy as np

from src.network.training.models.neural_models import model_gru
from src.network.training.tokenizers.tokenizers import tokenizer

# Класс функций и dispatcher состояний ACTION
from src.speech_recognition.speech_recognition import voice_processing


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


def voice_actions_switcher(action) -> str:
    switcher = {
        0: "Запись на занятие",
        1: "Подробнее",
        2: "Услуги",
        3: "Узнать уровень"
    }

    return switcher.get(action, "no_such_action")


# Обработка голосовых сообщений
def action_voice_func(update: Update, context: CallbackContext) -> int:
    """Reply that received a voice message."""
    # Получаем пользователя
    user = update.message.from_user.full_name
    logger.info("<%s> entered voice message.", user)
    # Получаем голосовой файл из Telegram
    file = context.bot.getFile(update.message.voice.file_id)

    # Директория корневого каталога
    dir_path = Path.cwd().parent

    # Директории источника и результата
    source_path = str(Path(dir_path, 'conversion', 'oggFiles', 'voice.ogg'))
    result_path = str(Path(dir_path, 'conversion', 'wavFiles', 'voice.wav'))

    # Скачиваем голосовой файл и помещаем в oggFiles
    file.download(custom_path=source_path)

    # Берем из oggFiles и конвертируем в wav, помещая в wavFiles
    opus_to_wav(source_path, result_path)

    # Отправляем на обработку в нейросеть
    i = voice_processing(result_path, tokenizer, model_gru)

    # Сопоставляем числовой ответ с текстовым
    text = voice_actions_switcher(i)
    print('bot choose to answer: ' + text)

    # Вызов ACTION dispatcher
    bot_action_functions = ActionFunctions()

    return bot_action_functions.actions_dispatcher(text, update, context)
