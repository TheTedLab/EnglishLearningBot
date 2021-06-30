import logging
import numpy as np

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

info_file_handler = logging.FileHandler("../logs/command_recognition_info.log", 'w', 'utf-8')
info_file_handler.setFormatter(formatter)

info_logger = logging.getLogger("command_recognition_info")
info_logger.setLevel(logging.INFO)
info_logger.addHandler(info_file_handler)

warn_file_handler = logging.FileHandler("../logs/command_recognition_warn.log", 'w', 'utf-8')
warn_file_handler.setFormatter(formatter)

warn_logger = logging.getLogger("command_recognition_warn")
warn_logger.setLevel(logging.WARNING)
warn_logger.addHandler(warn_file_handler)

critical_distance = 0.1


def save_in_log(command: str, percents: np.ndarray, choice: str):
    message = 'Command: ' + command + '; Result: ' \
              + choice + '; Predictions: ' + str(percents)

    info_logger.info(message)

    percents = percents[0, :]
    first = np.argmax(percents)
    second = 0

    for i in range(0, np.size(percents)):
        if int(percents.item(i)) > second & int(percents.item(i)) != first:
            second = np.where(percents == i)

    if first - second < critical_distance:
        warn_logger.info(message)
