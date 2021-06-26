import json

import numpy as np
import requests
from keras_preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from src.bot.authorization import wit_access_token
from src.bot.constants import API_ENDPOINT
# from src.speech_recognition.tts import tts


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
def voice_processing(result_path: str, tokenizer: Tokenizer, net_model) -> np.ndarray:
    with open(result_path, 'rb') as voice_file:
        voice_data = voice_file.read()

    text = recognize_speech(voice_data)
    print('bot heard: ' + text)

    sequence = tokenizer.texts_to_sequences([text])
    data = pad_sequences(sequence, maxlen=10)
    result = net_model.predict(data)

    return np.argmax(result)

    # Оставил на будущее, если будем делать ответы
    # tts.save_to_file(commands_dict.get(i, 'не понял'), '../resources/answer.ogg')
    # tts.runAndWait()
    # time.sleep(0.3)
    # answer = open('../resources/answer.ogg', 'rb')
    # update.message.reply_voice(answer)
