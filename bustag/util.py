import logging
import os
import configparser

logger = logging.getLogger('bustag')

DATA_PATH = './data/'
CONFIG_FILE = 'config.ini'
APP_CONFIG = {}


def setup_logging():
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)


def get_data_path(file):
    file_path = os.path.join(DATA_PATH, file)
    return file_path


def load_config():
    config_path = get_data_path(CONFIG_FILE)
    conf = configparser.ConfigParser()
    conf.read(config_path)
    for section in conf.sections():
        for key in conf.options(section):
            value = conf.get(section, key)
            key = section + '.' + key
            APP_CONFIG[key.lower()] = value


def init():
    setup_logging()
    load_config()


init()
