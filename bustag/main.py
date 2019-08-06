'''
entry point for command line 
'''
from bustag.model.prepare import prepare_predict_data
from bustag.spider.db import Item, ItemRate, RATE_TYPE
import bustag.model.classifier as clf
from bustag.util import logger


def recommend():
    '''
    system predict and update database
    '''
    ids, X = prepare_predict_data()
    y_pred = clf.predict(X)
    rate_type = RATE_TYPE.SYSTEM_RATE
    count = len(ids)
    recommend_count = sum(y_pred)
    for id, target in zip(ids, y_pred):
        item = Item.getit(id)
        ItemRate.saveit(rate_type, target, item)
    logger.debug(
        f'predicted {count} items, recommended {recommend_count}')
    return count, recommend_count
