import logging
import os
import sys
import configparser
import pytz
import datetime
from urllib.parse import urljoin

logger = logging.getLogger('bustag')
TESTING = False
DATA_PATH = 'data/'
CONFIG_FILE = 'config.ini'
MODEL_PATH = 'model/'
APP_CONFIG = {}
DEFAULT_CONFIG = {
    'download': {
        'count': 100,
        'interval': 3600
    }
}


def get_cwd():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.getcwd()


def check_testing():
    global TESTING
    if os.environ.get('TESTING'):
        TESTING = True
        print('*** in test mode ***')


def setup_logging():
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s \n %(message)s '
    formatter = logging.Formatter(fmt)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.WARNING)
    if TESTING:
        logger.setLevel(logging.DEBUG)
        pw_logger = logging.getLogger('peewee')
        pw_logger.addHandler(logging.StreamHandler())
        pw_logger.setLevel(logging.DEBUG)


def get_data_path(file):
    cwd = get_cwd()
    file_path = os.path.join(cwd, DATA_PATH, file)
    return file_path


def get_now_time():
    return datetime.datetime.now()


def get_full_url(path):
    root_path = APP_CONFIG['download.root_path']
    full_url = urljoin(root_path, path)
    return full_url


def check_config():
    config_path = get_data_path(CONFIG_FILE)
    abs_path = os.path.abspath(config_path)
    if not os.path.exists(abs_path):
        logger.error(
            f'file {abs_path} not exists,  please make sure file exists and configed, system quit now!')
        logger.error(f'文件 {abs_path} 不存在, 请检查文件存在并已配置, 系统退出!')
        sys.exit(1)


def load_config():
    check_config()
    config_path = get_data_path(CONFIG_FILE)
    conf = configparser.ConfigParser()
    conf.read_dict(DEFAULT_CONFIG)
    conf.read(config_path)
    for section in conf.sections():
        APP_CONFIG[section.lower()] = dict(conf[section])
        for key in conf.options(section):
            value = conf.get(section, key)
            key = section + '.' + key
            APP_CONFIG[key.lower()] = value
    logger.debug(APP_CONFIG)


def format_datetime(dt):
    format = '%Y-%m-%d %H:%M:%S'
    return dt.strftime(format)


def to_localtime(utc_dt):
    local_tz = pytz.timezone('Asia/Shanghai')
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    format = '%Y-%m-%d %H:%M:%S'
    local_dt = local_tz.normalize(local_dt)
    return local_dt.strftime(format)


def check_model_folder():
    model_path = os.path.join(DATA_PATH, MODEL_PATH)
    abs_path = os.path.abspath(model_path)
    if not os.path.exists(abs_path):
        print(f'created model folder: {abs_path}')
        os.mkdir(abs_path)


def init():
    print(f'CWD: {get_cwd()}')
    check_testing()
    setup_logging()
    load_config()
    check_model_folder()


init()
