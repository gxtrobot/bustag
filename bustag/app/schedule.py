import sys
import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from aspider import aspider
from bustag.spider import bus_spider
from bustag.util import logger, APP_CONFIG
import bustag.model.classifier as clf


def download(loop):
    """
    下载更新数据
    """
    print('start download')
    sys.argv = sys.argv[:1]
    sys.argv.append(APP_CONFIG['download.root_path'])
    bus_spider.reset_download()
    aspider.main(loop)
    try:
        clf.recommend()
    except FileNotFoundError:
        print('还没有训练好的模型, 无法推荐')


def start_scheduler():
    interval = int(APP_CONFIG['download.interval']) or 1800
    loop = asyncio.new_event_loop()
    scheduler = AsyncIOScheduler(event_loop=loop)
    trigger = IntervalTrigger(seconds=interval)
    t1 = datetime.now() + timedelta(seconds=10)
    # add for down at server start
    scheduler.add_job(download, 'date', run_date=t1, args=(loop,))
    scheduler.add_job(download, trigger=trigger, args=(loop,))
    scheduler.start()
    asyncio.set_event_loop(loop)
    loop.run_forever()
