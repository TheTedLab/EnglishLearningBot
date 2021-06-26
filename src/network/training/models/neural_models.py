import tensorflow
from tensorflow.keras.models import load_model

from src.bot.constants import (
    lstm_path,
    cnn_path,
    final_path
)

model_lstm = load_model(lstm_path)
model_cnn = load_model(cnn_path)
model_gru = tensorflow.keras.models.load_model(final_path)
