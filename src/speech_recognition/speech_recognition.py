import json

import numpy as np
import requests
from telegram import Update
from telegram.ext import CallbackContext
from tensorflow.keras.preprocessing.sequence import pad_sequences

from src.bot.authorization import wit_access_token
from src.bot.constants import API_ENDPOINT
from src.network.neural_models import model_gru
from src.network.tokenizer import tokenizer
from src.speech_recognition.tts import tts
from src.logs.loggers import save_in_log


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
def voice_processing(update: Update, context: CallbackContext,
                     result_path: str):
    with open(result_path, 'rb') as voice_file:
        voice = voice_file.read()

    text = recognize_speech(voice)
    update.message.reply_text(
        'Бот услышал: ' + text
    )
    print('bot heard: ' + text)

    command = text
    sequence = tokenizer.texts_to_sequences([command])
    text_data = pad_sequences(sequence, maxlen=10)
    result = model_gru.predict(text_data)
    update.message.reply_text(
        'Проценты: \n'
        '| Запись | Подробнее | Услуги | Уровень |\n' +
        str(result)
    )
    print(result)

    i = np.argmax(result)

    commands_dict = {
        0: 'записываю на занятие',
        1: 'говорю подробнее',
        2: 'показываю услуги',
        3: 'проверяю твой уровень'
    }

    update.message.reply_text(
        'Бот выбрал: ' + commands_dict.get(i, 'не понял')
    )
    print('bot choose to answer: ' + commands_dict.get(i, 'не понял'))

    save_in_log(command, result, commands_dict)
    tts.save_to_file(commands_dict.get(i, 'не понял'), '../resources/answer.ogg')
    tts.runAndWait()
    # time.sleep(0.3)
    answer = open('../resources/answer.ogg', 'rb')
    update.message.reply_voice(answer)
