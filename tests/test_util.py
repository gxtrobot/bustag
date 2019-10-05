from datetime import datetime
import configparser
from bustag import util


def test_file_path():
    file = 'bus.db'
    path = util.get_data_path(file)
    print(path)


def test_read_config():
    util.load_config()
    print(util.APP_CONFIG)


def test_to_localtime():
    t = datetime.utcnow()
    local = util.to_localtime(t)
    print(local)


def test_testing_mode():
    import os
    print(f'env: {os.getenv("TESTING")}')
    assert util.TESTING == True


def test_config_defaults():
    config_path = util.get_data_path(util.CONFIG_FILE)
    conf = configparser.ConfigParser()
    defaults = {
        'options': {
            'proxy': 'http://localhost:7890'
        },
        'download': {
            'count': 100,
            'interval': 3600
        }
    }
    conf.read_dict(defaults)
    conf.read(config_path)
    for section in conf:
        print(f'[{section}]')
        for key, value in conf[section].items():
            print(f'{key} = {value}')
        print('')
    print(conf.get('download', 'count'))
    print(conf.get('download', 'interval'))
    print(conf.get('options', 'proxy'))
