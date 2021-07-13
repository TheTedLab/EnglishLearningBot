import pickle

from src.bot.constants import (
    main_tokenizer_path,
    yes_no_tokenizer_path,
    services_tokenizer_path,
    times_tokenizer_path
)

with open(main_tokenizer_path, 'rb') as main_token:
    tokenizer = pickle.load(main_token)

with open(yes_no_tokenizer_path, 'rb') as yes_no_token:
    tokenizer_yn = pickle.load(yes_no_token)

with open(services_tokenizer_path, 'rb') as services_token:
    tokenizer_services = pickle.load(services_token)

with open(times_tokenizer_path, 'rb') as times_token:
    tokenizer_times = pickle.load(times_token)
