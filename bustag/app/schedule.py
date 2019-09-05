import sys
import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from aspider import aspider
from bustag.spider import bus_spider
from bustag.util import logger, APP_CONFIG


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
        import bustag.model.classifier as clf

        clf.recommend()
    except FileNotFoundError:
        print('还没有训练好的模型, 无法推荐')


def start_scheduler():
    interval = int(APP_CONFIG.get('download.interval', 1800))
    loop = asyncio.new_event_loop()
    scheduler = AsyncIOScheduler(event_loop=loop)
    t1 = datetime.now() + timedelta(seconds=10)
    int_trigger = IntervalTrigger(seconds=interval)
    date_trigger = DateTrigger(run_date=t1)
    # add for down at server start
    scheduler.add_job(download, trigger=date_trigger, args=(loop,))
    scheduler.add_job(download, trigger=int_trigger, args=(loop,))
    scheduler.start()
    asyncio.set_event_loop(loop)
    loop.run_forever()
