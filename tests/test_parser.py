import asyncio
import pytest
import aiohttp
from bustag.spider.parser import parse_item
from aspider.routeing import get_router


@pytest.fixture
def html():
    # url = 'https://www.cdnbus.bid/SHKD-875'
    url = 'https://www.busdmm.work/DVAJ-419'
    router = get_router()
    router.add_root_path(url.rsplit('/')[0])

    async def fetch(session, url):
        async with session.get(url) as response:
            return await response.text(errors='ignore')

    async def main():
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, url)
            return html

    html = asyncio.run(main())
    return html


def test_process_item(html):
    print('')
    meta, tags = parse_item(html)
    print(meta)
    print(tags)
