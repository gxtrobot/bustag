from bustag.model.persist import load_model, dump_model


def test_load_model():
    mlb = load_model()
    assert len(mlb.classes_) > 0
    print(mlb.classes_[:10])
    print(f'total tags: {len(mlb.classes_)}')
