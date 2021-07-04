import pandas as pd
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer


def improve_dataset(textPath, datasetPath):
    file1 = open(textPath, "r")
    print("aboba")
    dataset = pd.read_csv(datasetPath,
                        header=None,
                        names=['class', 'text'])

    text = dataset['text']
    tokenizer = Tokenizer(num_words=518)
    tokenizer.fit_on_texts(text)

    f = open(datasetPath, 'a')
    while True:
        # считываем строку
        word = file1.readline().strip()
        # прерываем цикл, если строка пустая
        if not word:
            break

        # выводим строку
        if tokenizer.word_index.get(word) is None:
            f.write("\n\"5\", \"" + word + "\"")

    # закрываем файл
    file1.close()
