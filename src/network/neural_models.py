from tensorflow.keras.models import load_model

from src.bot.constants import model_lstm_save_path, model_cnn_save_path, model_gru_save_path

model_lstm = load_model(model_lstm_save_path)
model_cnn = load_model(model_cnn_save_path)
model_gru = load_model(model_gru_save_path)
