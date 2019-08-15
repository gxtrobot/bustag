from bustag.spider.bus_spider import process_item
from aspider.routeing import get_router
from requests_html import HTMLSession
import logging


def test_process_item():
    root_path = 'https://www.cdnbus.bid'
    url = 'https://www.cdnbus.bid/CESD-797'
    session = HTMLSession()
    router = get_router()
    router.add_root_path(root_path)
    fanhao = 'CESD-797'
    r = session.get(url)
    process_item(r.text, url, fanhao)
