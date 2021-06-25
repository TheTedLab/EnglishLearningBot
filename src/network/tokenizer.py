import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer

from src.bot.constants import num_words, train_file_name

train = pd.read_csv(train_file_name,
                    header=None,
                    names=['class', 'text'])

text = train['text']

tokenizer = Tokenizer(num_words=num_words)
tokenizer.fit_on_texts(text)
