from bustag.spider.db import get_items, Item, RATE_TYPE, RATE_VALUE
from requests_html import HTMLSession, HTML
from bustag.spider.parser import parse_item


def test_get_items():
    rate_type = RATE_TYPE.SYSTEM_RATE
    rate_value = RATE_VALUE.DISLIKE
    page = None
    items, page_info = get_items(
        rate_type=rate_type, rate_value=rate_value, page=page)
    assert len(items) > 0
    print(f'item count:{len(items)}')
    print(
        f'total_items: {page_info[0]}, total_page: {page_info[1]}, current_page: {page_info[2]}, page_size:{page_info[3]}')


def test_get_items2():
    rate_type = None
    rate_value = None
    page = None
    items, page_info = get_items(
        rate_type=rate_type, rate_value=rate_value, page=page)
    assert len(items) > 0
    print(f'item count:{len(items)}')
    print(
        f'total_items: {page_info[0]}, total_page: {page_info[1]}, current_page: {page_info[2]}, page_size:{page_info[3]}')


def test_getit():
    id = 100
    item = Item.getit(id)
    print(repr(item))
    assert item is not None


def test_load_item():
    id = 1251
    item = Item.getit(id)
    Item.loadit(item)
    print(item.tags)


def test_get_item_tags():
    fanhao = 'JUY-981'
    item = Item.get_by_fanhao(fanhao)
    print(item)
    Item.get_tags_dict(item)
    print(item.tags_dict)


def test_missed_tags():
    url_temp = 'https://www.cdnbus.bid/{}'
    session = HTMLSession()
    num = 300
    i = 0
    fanhaos = ['PPPD-759', 'PPBD-166', 'XVSR-490', 'PPBD-162',
               'XVSR-478', 'BMW-188', 'GVG-935', 'TIKC-037', 'OVG-111', 'TIKF-037']
    # for item in Item.select().where(Item.fanhao.in_(fanhaos)):
    for item in Item.select():
        fanhao = item.fanhao
        url = url_temp.format(fanhao)
        r = session.get(url)
        meta, tags = parse_item(r.text)
        tags_set = {t.value for t in tags}
        # print(tags_set)
        tags_db = {t.tag.value for t in item.tags_list}
        # print(tags_db)
        diff = tags_set - tags_db
        if diff:
            print(f'{fanhao}tags not equal: {diff}')
        # else:
        #     print('tags are equal')
        i += 1
        if i > num:
            break


def test_empty_tags():
    empty = []
    for item in Item.select():
        tags_db = {t.tag.value for t in item.tags_list}
        if not tags_db:
            empty.append(item.fanhao)
    print(empty)
