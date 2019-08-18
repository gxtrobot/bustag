from datetime import datetime
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
