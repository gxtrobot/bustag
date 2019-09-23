import pytest
from requests_html import HTMLSession, HTML
from bustag.spider.parser import parse_item


@pytest.fixture
def html():
    # url = 'https://www.cdnbus.bid/SHKD-875'
    # url = 'https://www.cdnbus.bid/CESD-797'
    url = 'https://www.cdnbus.bid/JUY-985'
    session = HTMLSession()
    r = session.get(url)
    return r.text


def test_process_item(html):
    print('')
    meta, tags = parse_item(html)
    print(meta)
    print(tags)
