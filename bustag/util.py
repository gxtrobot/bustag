import logging
import os

logger = logging.getLogger('bustag')

DATA_PATH = './data/'


def setup_logging():
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)


def get_data_path(file):
    file_path = os.path.join(DATA_PATH, file)
    return file_path


setup_logging()
