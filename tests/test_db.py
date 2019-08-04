from bustag.spider.db import get_items


def test_get_items():
    items, page_info = get_items()
    assert len(items) > 0
    print()
    print(f'item count:{len(items)}')
    print(
        f'total_items: {page_info[0]}, total_page: {page_info[1]}, current_page: {page_info[2]}, page_size:{page_info[3]}')
