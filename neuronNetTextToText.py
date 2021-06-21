from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import utils
import pandas as pd

# Максимальное количество слов
num_words = 10000
# Максимальная длина текста
max_text_len = 30
# Количество классов текста
nb_classes = 8

train = pd.read_csv('train.csv',
                    header=None,
                    names=['class', 'question', 'text'])

text = train['text']
print(text[:8])
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
print(x_train[:8])
print('---------------------------')

model_lstm = Sequential()
model_lstm.add(Embedding(num_words, 32, input_length=max_text_len))
model_lstm.add(LSTM(16))
model_lstm.add(Dense(nb_classes, activation='softmax'))

model_lstm.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model_lstm_save_path = 'best_model_lstm.h5'
checkpoint_callback_lstm = ModelCheckpoint(model_lstm_save_path,
                                      monitor='val_accuracy',
                                      save_best_only=True,
                                      verbose=1)

history_lstm = model_lstm.fit(x_train,
                              y_train,
                              epochs=5,
                              batch_size=128,
                              validation_split=0.1,
                              callbacks=[checkpoint_callback_lstm])

test = pd.read_csv('test.csv',
                    header=None,
                    names=['class', 'title', 'text'])

test = pd.read_csv('test.csv',
                    header=None,
                    names=['class', 'title', 'text'])

test_sequences = tokenizer.texts_to_sequences(test['text'])
x_test = pad_sequences(test_sequences, maxlen=max_text_len)

y_test = utils.to_categorical(test['class'] - 1, nb_classes)
model_lstm.load_weights(model_lstm_save_path)
model_lstm.evaluate(x_test, y_test, verbose=1)
