import neuronNetTextToText
from src.network.training.net_constants import (
    dataset_file_path,
    model_lstm_save_path,
    model_cnn_save_path,
    model_gru_save_path,
    final_model_save_path,
    tokenizer_save_path,
    test_file_name,
    train_file_name,
    num_words,
    max_text_len,
    nb_classes
)

if __name__ == "__main__":
    neuronNetTextToText.train_net(dataset_file_path, model_lstm_save_path, model_cnn_save_path,
                                  model_gru_save_path, final_model_save_path, tokenizer_save_path,
                                  test_file_name, train_file_name, num_words, max_text_len, nb_classes)
