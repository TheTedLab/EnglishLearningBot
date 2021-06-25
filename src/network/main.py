import neuronNetTextToText

if __name__ == "__main__":
    neuronNetTextToText.train_net('dataset.txt', 'best_model_lstm.h5',
                                  'best_model_cnn.h5', 'best_model_gru.h5',
                                  'model_gru', 'tokenizer.pickle', 10000, 20, 4)
