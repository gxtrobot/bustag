'''
handle local file related functions
'''
from bustag.spider.db import Item, LocalItem, ItemRate, RATE_TYPE, RATE_VALUE, db
from bustag.util import logger


def add_local_fanhao(fanhao, tag_like):
    '''
    Args:
        fanhao:str - ',' separeted (fanhao, path)
    '''
    rows = fanhao.splitlines()
    items = []
    missed_fanhaos = []
    local_file_added = 0
    tag_file_added = 0
    for row in rows:
        if ',' in row:
            fanhao, path = row.split(',')
        else:
            fanhao = row
            path = None
        fanhao = fanhao.strip().upper()
        path = path.strip() if path else None
        items.append((fanhao, path))
    with db.atomic():
        for item in items:
            fanhao, path = item
            # if path is not None, add to local item
            if path:
                local_item = LocalItem.saveit(fanhao, path)
                if local_item:
                    local_file_added += 1
            # if tag_like is True, add it to item_rate table
            if tag_like:
                item_rate = ItemRate.saveit(
                    RATE_TYPE.USER_RATE, RATE_VALUE.LIKE, fanhao)
                if item_rate:
                    tag_file_added += 1
            if not Item.get_by_fanhao(fanhao):
                # add to get from spider
                missed_fanhaos.append(fanhao)
    logger.debug(f'missed_fanhaos:{missed_fanhaos}')
    logger.debug(f'tag_file_added:{tag_file_added}')
    logger.debug(f'local_file_added:{local_file_added}')
    return missed_fanhaos, local_file_added, tag_file_added
