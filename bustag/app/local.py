'''
handle local file related functions
'''
from bustag.spider.db import Item, LocalItem
from bustag.util import logger


def add_local_fanhao(fanhao):
    '''
    Args:
        fanhao:str - ',' separeted (fanhao, path)
    '''
    rows = fanhao.splitlines()
    items = []
    missed_fanhaos = []
    for row in rows:
        if ',' in row:
            fanhao, path = row.split(',')
        else:
            fanhao = row
            path = ''
        items.append((fanhao, path))
    for item in items:
        fanhao, path = item
        LocalItem.saveit(fanhao, path)
        if not Item.get_by_fanhao(fanhao):
            # add to get from spider
            missed_fanhaos.append(fanhao)
    logger.debug(f'missed_fanhaos:{missed_fanhaos}')
    return missed_fanhaos
