import matplotlib.pyplot as plt
import pandas as pd
from tensorflow.keras import utils
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Dense, Embedding, Conv1D, GlobalMaxPooling1D, LSTM, GRU
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import pickle
from src.network.training import datasetRandDivision


def init_lstm(num_words: int, max_text_len: int, nb_classes: int):
    model_lstm = Sequential()
    model_lstm.add(Embedding(num_words, 32, input_length=max_text_len))
    model_lstm.add(LSTM(16))
    model_lstm.add(Dense(nb_classes, activation='softmax'))
    return model_lstm


def init_cnn(num_words: int, max_text_len: int, nb_classes: int):
    model_cnn = Sequential()
    model_cnn.add(Embedding(num_words, 32, input_length=max_text_len))
    model_cnn.add(Conv1D(250, 5, padding='valid', activation='relu'))
    model_cnn.add(GlobalMaxPooling1D())
    model_cnn.add(Dense(128, activation='relu'))
    model_cnn.add(Dense(nb_classes, activation='softmax'))
    return model_cnn


def init_gru(num_words: int, max_text_len: int, nb_classes: int):
    model_gru = Sequential()
    model_gru.add(Embedding(num_words, 32, input_length=max_text_len))
    model_gru.add(GRU(16))
    model_gru.add(Dense(nb_classes, activation='softmax'))
    return model_gru


def train_model(model_save_path: str, model, x_train, y_train):
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    checkpoint_callback = ModelCheckpoint(model_save_path,
                                          monitor='val_accuracy',
                                          save_best_only=True,
                                          verbose=1)

    history = model.fit(x_train,
                        y_train,
                        epochs=1500,
                        batch_size=128,
                        validation_split=0.1,
                        callbacks=[checkpoint_callback])

    plt.plot(history.history['accuracy'],
             label='Доля верных ответов на обучающем наборе')
    plt.plot(history.history['val_accuracy'],
             label='Доля верных ответов на проверочном наборе')
    plt.xlabel('Эпоха обучения')
    plt.ylabel('Доля верных ответов')
    plt.legend()
    plt.show()


def evaluate_model(model, model_save_path, x_test, y_test):
    model.load_weights(model_save_path)
    return model.evaluate(x_test, y_test, verbose=1)


def train_net(dataset_name: str, model_lstm_save_path: str, model_cnn_save_path: str,
              model_gru_save_path: str, final_model_save_path: str, tokenizer_save_path: str,
              test_file_name: str, train_file_name: str, num_words: int,
              max_text_len: int, nb_classes: int):
    """ trainFileName: The name of the training data file with the extension .csv (Example: train.csv)
    testFileName: The name of the data file for the test with the extension .csv (Example: test.csv)
    modelLstmSavePath: The name of the file to save the resulting LSTM model with the extension .h5
    (Example: best_model_lstm.h5)
    modelCnnSavePath: The name of the file to save the resulting Conv model with the extension .h5
    (Example: best_model_cnn.h5)
    modelGruSavePath: The name of the file to save the resulting GRU model with the extension .h5
    (Example: best_model_gru.h5)
    numWords: Maximum number of words (Std value: 10000)
    maxTextLen: Maximum text length (Std value: 20)
    nbClasses: Number of text classes (Std value: 4)
        """

    datasetRandDivision.divide_dataset(dataset_name)

    train = pd.read_csv(train_file_name,
                        header=None,
                        names=['class', 'text'])

    text = train['text']
    print(text[:5])
    print('---------------------------')

    y_train = utils.to_categorical(train['class'], nb_classes)
    print(y_train)
    print('---------------------------')

    tokenizer = Tokenizer(num_words=num_words)
    tokenizer.fit_on_texts(text)
    print(tokenizer.word_index)
    print('---------------------------')

    sequences = tokenizer.texts_to_sequences(text)
    index = 1
    print(text[index])
    print(sequences[index])
    print('---------------------------')

    x_train = pad_sequences(sequences, maxlen=max_text_len)
    print(x_train[:5])
    print('---------------------------')

    model_lstm = init_lstm(num_words, max_text_len, nb_classes)
    train_model(model_lstm_save_path, model_lstm, x_train, y_train)

    print("\n\nConv\n")
    model_cnn = init_cnn(num_words, max_text_len, nb_classes)
    train_model(model_cnn_save_path, model_cnn, x_train, y_train)

    print("\n\nGRU\n")
    model_gru = init_gru(num_words, max_text_len, nb_classes)
    train_model(model_gru_save_path, model_gru, x_train, y_train)

    test = pd.read_csv(test_file_name,
                       header=None,
                       names=['class', 'text'])

    test_sequences = tokenizer.texts_to_sequences(test['text'])
    x_test = pad_sequences(test_sequences, maxlen=max_text_len)

    y_test = utils.to_categorical(test['class'], nb_classes)

    evaluate_model(model_lstm, model_lstm_save_path, x_test, y_test)
    evaluate_model(model_cnn, model_cnn_save_path, x_test, y_test)
    evaluate_model(model_gru, model_gru_save_path, x_test, y_test)

    model_gru.save(final_model_save_path)

    with open(tokenizer_save_path, 'wb') as f:
        pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)
