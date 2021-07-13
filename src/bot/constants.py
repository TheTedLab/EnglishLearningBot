# UTF-8 коды для эмодзи
hand_emoji = u'\U0001F44B'
check_mark = u'\U00002705'
cross_mark = u'\U0000274C'
right_triangle = u'\U000025B6'
memo_emoji = u'\U0001F4DD'
loudspeaker = u'\U0001F4E2'

# Перечисление состояний разговора
ACTION, RECORD, TIME_SIGN, INFO, SERVICES, SERVICE_SELECTION, LEVEL_KNOWLEDGE, \
    LEVEL_LANGUAGE, TEACHER_INFO = range(9)

# Константы распознавания речи
API_ENDPOINT = 'https://api.wit.ai/speech'
RU_VOICE_ID = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"

# Пути к файлам нейронных сетей для бота
lstm_path = '../network/training/training_files/best_model_lstm.h5'
cnn_path = '../network/training/training_files/best_model_cnn.h5'

# Модели нейросетей
main_model_path = '../network/training/models/model_gru'
yes_no_model_path = '../network/training/models/model_gru_yn'
services_model_path = '../network/training/models/model_gru_services'
times_model_path = '../network/training/models/model_gru_times'

# Токенайзеры
main_tokenizer_path = '../network/training/tokenizers/tokenizer.pickle'
yes_no_tokenizer_path = '../network/training/tokenizers/tokenizer_yn.pickle'
services_tokenizer_path = '../network/training/tokenizers/tokenizer_services.pickle'
times_tokenizer_path = '../network/training/tokenizers/tokenizer_times.pickle'
