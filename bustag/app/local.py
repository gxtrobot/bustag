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
    local_file_added = 0
    for row in rows:
        if ',' in row:
            fanhao, path = row.split(',')
        else:
            fanhao = row
            path = None
        fanhao = fanhao.strip()
        path = path.strip() if path else None
        items.append((fanhao, path))
    for item in items:
        fanhao, path = item
        # if path is not None, add to local item
        if path:
            LocalItem.saveit(fanhao, path)
            local_file_added += 1
        if not Item.get_by_fanhao(fanhao):
            # add to get from spider
            missed_fanhaos.append(fanhao)
    logger.debug(f'missed_fanhaos:{missed_fanhaos}')
    return missed_fanhaos, local_file_added
