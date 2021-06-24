import matplotlib.pyplot as plt
import pandas as pd
from tensorflow.keras import utils
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Dense, Embedding, Conv1D, GlobalMaxPooling1D, LSTM, GRU
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer


def train_net(train_file_name: str, test_file_name: str, model_lstm_save_path: str, model_cnn_save_path: str,
              model_gru_save_path: str, num_words: int, max_text_len: int, nb_classes: int):
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

    train = pd.read_csv(train_file_name,
                        header=None,
                        names=['class', 'text'])

    text = train['text']
    print(text[:5])
    print('---------------------------')

    y_train = utils.to_categorical(train['class'] - 1, nb_classes)
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

    model_lstm = Sequential()
    model_lstm.add(Embedding(num_words, 32, input_length=max_text_len))
    model_lstm.add(LSTM(16))
    model_lstm.add(Dense(nb_classes, activation='softmax'))

    model_lstm.compile(optimizer='adam',
                       loss='categorical_crossentropy',
                       metrics=['accuracy'])

    checkpoint_callback_lstm = ModelCheckpoint(model_lstm_save_path,
                                               monitor='val_accuracy',
                                               save_best_only=True,
                                               verbose=1)

    history_lstm = model_lstm.fit(x_train,
                                  y_train,
                                  epochs=50,
                                  batch_size=128,
                                  validation_split=0.1,
                                  callbacks=[checkpoint_callback_lstm])

    test = pd.read_csv(test_file_name,
                       header=None,
                       names=['class', 'text'])

    test_sequences = tokenizer.texts_to_sequences(test['text'])
    x_test = pad_sequences(test_sequences, maxlen=max_text_len)

    y_test = utils.to_categorical(test['class'] - 1, nb_classes)
    model_lstm.load_weights(model_lstm_save_path)
    model_lstm.evaluate(x_test, y_test, verbose=1)

    plt.plot(history_lstm.history['accuracy'],
             label='Доля верных ответов на обучающем наборе')
    plt.plot(history_lstm.history['val_accuracy'],
             label='Доля верных ответов на проверочном наборе')
    plt.xlabel('Эпоха обучения')
    plt.ylabel('Доля верных ответов')
    plt.legend()
    plt.show()

    print("\n\nConv\n")
    model_cnn = Sequential()
    model_cnn.add(Embedding(num_words, 32, input_length=max_text_len))
    model_cnn.add(Conv1D(250, 5, padding='valid', activation='relu'))
    model_cnn.add(GlobalMaxPooling1D())
    model_cnn.add(Dense(128, activation='relu'))
    model_cnn.add(Dense(nb_classes, activation='softmax'))

    model_cnn.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

    checkpoint_callback_cnn = ModelCheckpoint(model_cnn_save_path,
                                              monitor='val_accuracy',
                                              save_best_only=True,
                                              verbose=1)

    history_cnn = model_cnn.fit(x_train,
                                y_train,
                                epochs=50,
                                batch_size=128,
                                validation_split=0.1,
                                callbacks=[checkpoint_callback_cnn])

    plt.plot(history_cnn.history['accuracy'],
             label='Доля верных ответов на обучающем наборе')
    plt.plot(history_cnn.history['val_accuracy'],
             label='Доля верных ответов на проверочном наборе')
    plt.xlabel('Эпоха обучения')
    plt.ylabel('Доля верных ответов')
    plt.legend()
    plt.show()

    print("\n\nGRU\n")
    model_gru = Sequential()
    model_gru.add(Embedding(num_words, 32, input_length=max_text_len))
    model_gru.add(GRU(16))
    model_gru.add(Dense(nb_classes, activation='softmax'))

    model_gru.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

    checkpoint_callback_gru = ModelCheckpoint(model_gru_save_path,
                                              monitor='val_accuracy',
                                              save_best_only=True,
                                              verbose=1)

    history_gru = model_gru.fit(x_train,
                                y_train,
                                epochs=50,
                                batch_size=128,
                                validation_split=0.1,
                                callbacks=[checkpoint_callback_gru])

    plt.plot(history_gru.history['accuracy'],
             label='Доля верных ответов на обучающем наборе')
    plt.plot(history_gru.history['val_accuracy'],
             label='Доля верных ответов на проверочном наборе')
    plt.xlabel('Эпоха обучения')
    plt.ylabel('Доля верных ответов')
    plt.legend()
    plt.show()
