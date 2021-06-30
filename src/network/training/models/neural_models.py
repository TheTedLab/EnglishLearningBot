import tensorflow
from tensorflow.keras.models import load_model

from src.bot.constants import (
    lstm_path,
    cnn_path,
    main_model_path,
    yes_no_model_path,
    services_model_path
)

model_lstm = load_model(lstm_path)
model_cnn = load_model(cnn_path)
model_gru = tensorflow.keras.models.load_model(main_model_path)
model_gru_yn = tensorflow.keras.models.load_model(yes_no_model_path)
model_gru_services = tensorflow.keras.models.load_model(services_model_path)
