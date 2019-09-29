import random
from bustag.model import classifier as clf
from bustag.model.prepare import prepare_predict_data
from bustag.spider.db import Item, get_items, ItemRate


def test_train_model():
    clf.train()


def test_recommend():
    total, count = clf.recommend()
    print('total:', total)
    print('recommended:', count)


def test_make_model():
    '''
    tag random data to generate model
    '''
    page = 50
    no_rate_items = []
    for i in range(1, page):
        items, _ = get_items(None, None, i)
        no_rate_items.extend(items)
    size = len(no_rate_items)
    like_ratio = 0.4
    like_items = []
    unlike_items = []
    for item in no_rate_items:
        if random.random() < like_ratio:
            like_items.append(item)
        else:
            unlike_items.append(item)
    print(f'like items: {len(like_items)}, unlike items: {len(unlike_items)}')
    for item in like_items:
        ItemRate.saveit(1, 1, item.fanhao)
    for item in unlike_items:
        ItemRate.saveit(1, 0, item.fanhao)

    clf.train()
