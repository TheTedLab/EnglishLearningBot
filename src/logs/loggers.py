import logging

import numpy as np

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

info_file_handler = logging.FileHandler("../logs/command_recognition_info.log", 'a', 'utf-8')
info_file_handler.setFormatter(formatter)

info_logger = logging.getLogger("command_recognition_info")
info_logger.setLevel(logging.INFO)
info_logger.addHandler(info_file_handler)

warn_file_handler = logging.FileHandler("../logs/command_recognition_warn.log", 'a', 'utf-8')
warn_file_handler.setFormatter(formatter)

warn_logger = logging.getLogger("command_recognition_warn")
warn_logger.setLevel(logging.INFO)
warn_logger.addHandler(warn_file_handler)

critical_distance = 0.97


def save_in_log(command: str, percents: np.ndarray, choice: str):
    message = 'Command: ' + command + '; Result: ' \
              + choice + ';\nPredictions: [['
    for i in range(percents.size):
        message += " %.9f" % percents.item(i)

    message += ']]'

    info_logger.info(message)

    percents = percents[0, :]
    first = float(np.max(percents))
    second = 0.0

    for i in range(0, np.size(percents)):
        index_percent = float(percents.item(i))
        if index_percent > second and index_percent != first:
            second = index_percent

    print('min diff: ' + str(first - second))
    if float(first - second) < critical_distance:
        warn_logger.info(message)
