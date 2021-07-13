import pyttsx3

from src.bot.constants import RU_VOICE_ID

tts = pyttsx3.init()
tts.setProperty('voice', RU_VOICE_ID)
