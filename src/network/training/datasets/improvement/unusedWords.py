import pandas as pd

from tensorflow.keras.preprocessing.text import Tokenizer
from src.network.training.datasets.improvement.text_constants import russian_dictionary
from src.network.training.net_constants import dataset_file_path


def improve_dataset(text_path, dataset_path):
    text_file = open(text_path, "r")
    print("open dataset file")
    dataset = pd.read_csv(dataset_path,
                          header=None,
                          names=['class', 'text'])

    text = dataset['text']
    tokenizer = Tokenizer(num_words=518)
    tokenizer.fit_on_texts(text)

    file = open(dataset_path, 'a')
    while True:
        # считываем строку
        word = text_file.readline().strip()
        # прерываем цикл, если строка пустая
        if not word:
            break

        # выводим строку
        if tokenizer.word_index.get(word) is None:
            file.write("\n\"5\", \"" + word + "\"")

    # закрываем файл
    text_file.close()


if __name__ == "__main__":
    improve_dataset(russian_dictionary, dataset_file_path)
