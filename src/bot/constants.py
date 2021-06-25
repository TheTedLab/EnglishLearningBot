# UTF-8 коды для эмодзи
hand_emoji = u'\U0001F44B'
check_mark = u'\U00002705'
cross_mark = u'\U0000274C'
right_triangle = u'\U000025B6'

# Перечисление состояний разговора
ACTION, RECORD, TIME_SIGN, INFO, SERVICES, SERVICE_SELECTION, LEVEL_KNOWLEDGE, \
    LEVEL_LANGUAGE, TEACHER_INFO = range(9)

# Константы распознавания речи
API_ENDPOINT = 'https://api.wit.ai/speech'
RU_VOICE_ID = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"

# Константы нейронных сетей
train_file_name = '../network/train.csv'
test_file_name = '../network/test.csv'
model_lstm_save_path = '../network/best_model_lstm.h5'
model_cnn_save_path = '../network/best_model_cnn.h5'
model_gru_save_path = '../network/best_model_gru.h5'
num_words = 10000
max_text_len = 20
nb_classes = 4
