import pickle

from src.bot.constants import tokenizer_path

with open(tokenizer_path, 'rb') as file:
    tokenizer = pickle.load(file)
