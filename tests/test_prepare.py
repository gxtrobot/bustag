from bustag.model.prepare import load_data, process_data, prepare_predict_data


def test_load_data():
    df = load_data()
    assert len(df) > 0
    print(df.iloc[0])


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
