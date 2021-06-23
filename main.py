from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, MaxPooling1D, Conv1D, GlobalMaxPooling1D, Dropout, LSTM, GRU
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import utils
import pandas as pd
import numpy as np
import random
import time
import telebot
import requests
import subprocess
import pyttsx3
import json

API_ENDPOINT = 'https://api.wit.ai/speech'

# Wit.ai api access token
wit_access_token = 'ZIJAR4WEPUZEVJHYEVZYUXLZZNZXKHQO'


TG_API = '1889784597:AAH9muA6PWCt4eGxEVeJn9KTSLRi_EVkJpQ'
bot = telebot.TeleBot(TG_API)

tts = pyttsx3.init()
RU_VOICE_ID = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
tts.setProperty('voice', RU_VOICE_ID)


command_classes = 4

with open("data.txt", "r") as f:
    data = f.read().split('\n')

random.shuffle(data)

print(data)


train_data = "\n"
test_data = "\n"

with open("train.csv", "w") as f:
    f.write(train_data.join(data[:200]))


with open("test.csv", "w") as f:
    f.write(test_data.join(data[200:]))


train = pd.read_csv('data.txt',
                    header=None,
                    names=['class', 'text'])
#
commands = train['text']
#
y_train = utils.to_categorical(train['class'] - 1, command_classes)
#
tokenizer = Tokenizer()
tokenizer.fit_on_texts(commands)
seqs = tokenizer.texts_to_sequences(commands)

x_train = pad_sequences(seqs, maxlen=10)

model_lstm = Sequential()
model_lstm.add(Embedding(1000, 32, input_length=10))
model_lstm.add(LSTM(16))
model_lstm.add(Dense(4, activation='softmax'))

model_lstm.compile(optimizer='adam',
               loss='categorical_crossentropy',
               metrics=['accuracy'])

model_lstm_save_path = 'best_model_lstm.h5'
checkpoint_callback_lstm = ModelCheckpoint(model_lstm_save_path,
                                       monitor='val_accuracy',
                                       save_best_only=True,
                                       verbose=1)

history_lstm = model_lstm.fit(x_train,
                            y_train,
                            epochs=1000,
                            batch_size=128,
                            validation_split=0.1,
                             callbacks=[checkpoint_callback_lstm])

test = pd.read_csv('test.csv',
                    header=None,
                    names=['class', 'text'])

test_sequences = tokenizer.texts_to_sequences(test['text'])
x_test = pad_sequences(test_sequences, maxlen=10)

y_test = utils.to_categorical(test['class'] - 1, 4)

model_lstm.load_weights(model_lstm_save_path)
res = model_lstm.evaluate(x_test, y_test, verbose=1)
print(res)




def RecognizeSpeech(audio):

    # defining headers for HTTP request
    headers = {'authorization': 'Bearer ' + wit_access_token,
               'Content-Type': 'audio/wav'}

    # making an HTTP post request
    resp = requests.post(API_ENDPOINT, headers=headers,
                         data=audio)

    # converting response content to JSON format
    data = json.loads(resp.content)

    # get text from data
    text = data['text']

    # return the text
    return text


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    file = bot.download_file(file_info.file_path)
    with open('voice.ogg', 'wb') as dfile:
        dfile.write(file)

    sourceFile = 'voice.ogg'
    resultFile = 'voice.wav'
    options = '--force-wav'
    cmd = 'opusdec.exe ' + options + ' ' + sourceFile + ' ' + resultFile
    subprocess.run(cmd)
    time.sleep(0.3)

    with open('voice.wav', 'rb') as f:
        voice = f.read()

    text = RecognizeSpeech(voice)
    print(text)

    command = text
    sequence = tokenizer.texts_to_sequences([command])
    data = pad_sequences(sequence, maxlen=10)
    result = model_lstm.predict(data)
    print(result)

    i = np.argmax(result)

    commands_dict = {0: 'записываю на занятие', 1: 'говорю подробнее',
                     2: 'показываю услуги', 3: 'проверяю твой уровень'}

    tts.save_to_file(commands_dict.get(i, 'не понял'), 'answer.ogg')
    tts.runAndWait()
    time.sleep(0.3)
    answer = open('answer.ogg', 'rb')
    bot.send_voice(message.chat.id, answer)


bot.polling()


