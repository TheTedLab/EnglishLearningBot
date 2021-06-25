import neuronNetTextToText

from src.bot.constants import (
    num_words,
    max_text_len,
    nb_classes,
    train_file_name,
    test_file_name,
    model_lstm_save_path,
    model_cnn_save_path,
    model_gru_save_path,
)

if __name__ == "__main__":
    neuronNetTextToText.train_net(train_file_name, test_file_name, model_lstm_save_path,
                                  model_cnn_save_path, model_gru_save_path,
                                  num_words, max_text_len, nb_classes)
