'''
define url routing process logic
'''
import sys
import os
import signal
from aspider.routeing import get_router
from .parser import parse_item
from .db import save
router = get_router()
counter = 0
SYSTEM_EXIT = False


def system_exit():
    global SYSTEM_EXIT
    if not SYSTEM_EXIT:
        SYSTEM_EXIT = True
        raise KeyboardInterrupt()


def verify_page_path(path, no):
    print(f'verify page {path} , args {no}')
    no = int(no)
    if no <= 10:
        return True
    else:
        return False


def check_exit():
    if counter > 100 and not SYSTEM_EXIT:
        system_exit()


@router.route('/page/<no>', verify_page_path)
def process_page(text, path, no):
    '''
    process list page
    '''
    print(f'page {no} has length {len(text)}')
    print(f'process page {no}')


@router.route('/<fanhao:[\w]+-[\d]+>')
def process_item(text, path, fanhao):
    '''
    process item page
    '''
    global counter
    counter += 1
    print(f'process item {fanhao}')
    url = router.get_full_url(path)
    meta, tags = parse_item(text)
    meta.update(url=url)
    print('meta keys', len(meta.keys()))
    print('tag count', len(tags))
    save(meta, tags)
    check_exit()


if __name__ == "__main__":
    from aspider import aspider
    import sys
    aspider.main()
