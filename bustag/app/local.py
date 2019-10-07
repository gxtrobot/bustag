'''
handle local file related functions
'''
import re
from peewee import SqliteDatabase, DatabaseError

from bustag.spider.db import Item, LocalItem, ItemRate, RATE_TYPE, RATE_VALUE, db, DBError
from bustag.util import logger, get_data_path


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
    pattern = r'([A-Z]+)-?([0-9]+)'
    for row in rows:
        if ',' in row:
            fanhao, path = row.split(',')
        else:
            fanhao = row
            path = None

        fanhao = fanhao.strip().upper()
        match = re.search(pattern, fanhao)
        if match and len(match.groups()) == 2:
            series, num = match.groups()
            matched_fanhao = f'{series}-{num}'
            path = path.strip() if path else None
            logger.debug(f'matched fanhao {matched_fanhao}')
            items.append((matched_fanhao, path))
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


def load_tags_db():
    '''
    load user tags data from uploaded db file

    Args:
        file: io.BufferedRandom -> uploaded db file stream
    '''
    db_name = get_data_path('uploaded.db')
    try:
        db_upload = SqliteDatabase(db_name)
        db_upload.get_tables()
    except DatabaseError:
        raise DBError()
    db_is_old = False
    tag_data = []
    missed_fanhaos = []
    tag_file_added = 0
    sql_old = '''select item_rate.rate_value, item.fanhao
                from item_rate inner
                join item on item_rate.item_id = item.id
                where item_rate.rate_type=1 '''

    sql_new = '''select item_rate.rate_value, item.fanhao
                from item_rate inner
                join item on item_rate.item_id = item.fanhao
                where item_rate.rate_type=1 '''
    cursor = db_upload.execute_sql(sql_old)
    res = cursor.fetchone()
    if res:
        db_is_old = True
    if db_is_old:
        cursor = db_upload.execute_sql(sql_old)
    else:
        cursor = db_upload.execute_sql(sql_new)

    for row in cursor.fetchall():
        tag_data.append(row)
    with db_upload.atomic():
        for rate_value, fanhao in tag_data:
            item_rate = ItemRate.saveit(
                RATE_TYPE.USER_RATE, rate_value, fanhao)
            if item_rate:
                tag_file_added += 1
            if not Item.get_by_fanhao(fanhao):
                # add to get from spider
                missed_fanhaos.append(fanhao)
    logger.debug(tag_data)
    logger.info(f'added user tag rate: {tag_file_added}')
    logger.info(f'added fanhao to download: {len(missed_fanhaos)}')
    return tag_file_added, missed_fanhaos
