'''
prepare data for model training
'''
import json
import operator
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from bustag.spider.db import get_items, RATE_TYPE, ItemRate, Item, get_tags_for_items
from bustag.model.persist import dump_model, load_model
from bustag.util import logger, get_data_path, MODEL_PATH

BINARIZER_PATH = MODEL_PATH + 'label_binarizer.pkl'


def load_data():
    '''
    load data from database and do processing
    '''
    rate_type = RATE_TYPE.USER_RATE.value
    rate_value = None
    page = None
    items, _ = get_items(rate_type=rate_type, rate_value=rate_value,
                         page=page)
    return items


def as_dict(item):
    tags_set = set()
    for tags in item.tags_dict.values():
        for tag in tags:
            tags_set.add(tag)
    d = {
        'id': item.fanhao,
        'title': item.title,
        'fanhao': item.fanhao,
        'url': item.url,
        'add_date': item.add_date,
        'tags': tags_set,
        'cover_img_url': item.cover_img_url,
        'target': item.rate_value
    }
    return d


def process_data(df):
    '''
    do all processing , like onehotencode tag string
    '''
    X = df[['tags']]
    y = df[['target']]

    mlb = MultiLabelBinarizer()
    X = mlb.fit_transform(X.tags.values)
    dump_model(get_data_path(BINARIZER_PATH), mlb)
    return X, y


def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42)
    return (X_train, X_test, y_train, y_test)


def prepare_data():
    items = load_data()
    dicts = (as_dict(item) for item in items)
    df = pd.DataFrame(dicts, columns=['id', 'title', 'fanhao', 'url', 'add_date', 'tags', 'cover_img_url',
                                      'target'])
    X, y = process_data(df)
    return split_data(X, y)


def prepare_predict_data():
    # get not rated data
    rate_type = None
    rate_value = None
    page = None
    unrated_items, _ = get_items(
        rate_type=rate_type, rate_value=rate_value, page=page)
    mlb = load_model(get_data_path(BINARIZER_PATH))
    dicts = (as_dict(item) for item in unrated_items)
    df = pd.DataFrame(dicts, columns=['id', 'tags'])
    df.set_index('id', inplace=True)
    X = mlb.transform(df.tags.values)
    return df.index.values, X
