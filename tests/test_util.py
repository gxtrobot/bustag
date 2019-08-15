from bustag import util


def test_file_path():
    file = 'bus.db'
    path = util.get_data_path(file)
    print(path)
