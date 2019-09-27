from bustag.model.prepare import load_data, process_data, prepare_predict_data


def test_load_data():
    items = load_data()
    print(len(items))
    item = items[0]
    print(item.fanhao, item.tags_dict)
    assert len(items) > 0


def test_process_data():
    df = load_data()
    X, y = process_data(df)
    print(X.shape)
    print(y.shape)


def test_prepare_predict_data():
    ids, X = prepare_predict_data()
    print(X.shape)
    print(X[0])
    print(ids)
