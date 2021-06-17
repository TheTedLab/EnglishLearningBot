import time
import telebot
import requests
import json
import pyttsx3


TG_API = '1889784597:AAH9muA6PWCt4eGxEVeJn9KTSLRi_EVkJpQ'
bot = telebot.TeleBot(TG_API)

URL = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
IAM = "t1.9euelZqRk5HOmI7GjZDHkc6Kzs_Iyu3rnpWazpjIkZLHyIyYi8fJnpKRjcnl9PccFVZ5-e8FYjSI3fT3XENTefnvBWI0iA.A-sWNkjVU2jkZ1Jgazu1ZsbmAuxvNmHPVWF62TigfQ6ayFtd4QpKTmGscmtq_nzoArDSY6-g-Qup-CHKhXSuBA"
ID = "b1g628fpciqlrvm7g00i"
YA_API = "AQVN1bXy8uunsrBMjQDdSUClHIuT4EmWakiqqAQS"


tts = pyttsx3.init()
RU_VOICE_ID = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
tts.setProperty('voice', RU_VOICE_ID)

def recognize(voice, IAM, ID):
    headers = {'Authorization': f'Api-Key {YA_API}'}

    # остальные параметры:
    params = {
        'lang': 'ru-RU',
        'folderId': ID,
        'sampleRateHertz': 48000,
    }

    response = requests.post(URL, params=params, headers=headers, data=voice)

    # бинарные ответ доступен через response.content, декодируем его:
    decode_resp = response.content.decode('UTF-8')

    # и загрузим в json, чтобы получить текст из аудио:

    text = json.loads(decode_resp)

    return text['result']


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    file = bot.download_file(file_info.file_path)
    with open('voice.ogg', 'wb') as dfile:
        dfile.write(file)

    with open('voice.ogg', 'rb') as f:
        voice = f.read()

    text = recognize(voice, IAM, ID)
    print(text)
    tts.save_to_file(text, 'answer.ogg')
    tts.runAndWait()
    time.sleep(0.3)
    answer = open('answer.ogg', 'rb')
    bot.send_voice(message.chat.id, answer)


bot.polling()
