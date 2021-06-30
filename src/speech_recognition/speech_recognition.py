import json

import numpy as np
import requests
from keras_preprocessing.text import Tokenizer
from pathlib import Path
from telegram import Update
from telegram.ext import CallbackContext
from tensorflow.keras.preprocessing.sequence import pad_sequences

from src.bot.authorization import wit_access_token
from src.bot.constants import API_ENDPOINT
from src.logs.loggers import save_in_log
from src.conversion.opusToWav import opus_to_wav


# from src.speech_recognition.tts import tts

# Предобработка голосового сообщения: скачивание и конвертация
def voice_pre_processing(update: Update, context: CallbackContext) -> str:
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

    return result_path


# Распознавание речи с помощью WIT AI API
def recognize_speech(audio):
    # defining headers for HTTP request
    headers = {
        'authorization': 'Bearer ' + wit_access_token,
        'Content-Type': 'audio/wav'
    }

    # making an HTTP post request
    resp = requests.post(API_ENDPOINT, headers=headers,
                         data=audio)

    # converting response content to JSON format
    voice_data = json.loads(resp.content)

    # get text from data
    text = voice_data['text']

    # return the text
    return text


# Обработка голосового сообщения
def voice_processing(result_path: str, tokenizer: Tokenizer, net_model, switcher) -> str:
    # Читаем wav-файл
    with open(result_path, 'rb') as voice_file:
        voice_data = voice_file.read()

    # Распознавание речи
    text = recognize_speech(voice_data)
    print('bot heard: ' + text)

    # Разбиваем на токены
    sequence = tokenizer.texts_to_sequences([text])
    data = pad_sequences(sequence, maxlen=10)

    # Нейросеть предсказывает ответ
    result = net_model.predict(data)
    i = np.argmax(result)

    # Сопоставляем числовой ответ с текстовым
    choice_text = switcher(i)
    print('bot choose to answer: ' + choice_text)

    # Сохраняем в лог
    save_in_log(text, result, choice_text)

    return choice_text

    # Оставил на будущее, если будем делать ответы
    # tts.save_to_file(commands_dict.get(i, 'не понял'), '../resources/answer.ogg')
    # tts.runAndWait()
    # time.sleep(0.3)
    # answer = open('../resources/answer.ogg', 'rb')
    # update.message.reply_voice(answer)
