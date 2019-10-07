'''
define url routing process logic
'''
import sys
import os
import signal
from aspider.routeing import get_router
from .parser import parse_item
from .db import save, Item
from bustag.util import APP_CONFIG, get_full_url, logger
router = get_router()
MAXPAGE = 30


def get_url_by_fanhao(fanhao):
    # return full url
    url = get_full_url(fanhao)
    return url


def verify_page_path(path, no):
    logger.debug(f'verify page {path} , args {no}')
    no = int(no)
    if no <= MAXPAGE:
        return True
    else:
        return False


@router.route('/page/<no>', verify_page_path)
def process_page(text, path, no):
    '''
    process list page
    '''
    logger.debug(f'page {no} has length {len(text)}')
    print(f'process page {no}')


def verify_fanhao(path, fanhao):
    '''
    verify fanhao before add it to queue
    '''
    exists = Item.get_by_fanhao(fanhao)
    logger.debug(
        f'verify {fanhao}: , exists:{exists is not None}, skip {path}')
    return exists is None


@router.route('/<fanhao:[\w]+-[\d]+>', verify_fanhao, no_parse_links=True)
def process_item(text, path, fanhao):
    '''
    process item page
    '''
    logger.debug(f'process item {fanhao}')
    url = path
    meta, tags = parse_item(text)
    meta.update(url=url)
#     logger.debug('meta keys', len(meta.keys()))
#     logger.debug('tag count', len(tags))
    save(meta, tags)
    print(f'item {fanhao} is processed')
