from bustag.model import classifier as clf
from bustag.model.prepare import prepare_predict_data


def test_train_model():
    clf.train()


def test_recommend():
    total, count = clf.recommend()
    print('total:', total)
    print('recommended:', count)
