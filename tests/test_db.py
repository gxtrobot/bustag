from bustag.spider.db import get_items, Item, RATE_TYPE, RATE_VALUE


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


def test_getit():
    id = 100
    item = Item.getit(id)
    print(repr(item))
    assert item is not None
