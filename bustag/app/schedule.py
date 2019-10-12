import sys
import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from aspider import aspider
from bustag.spider import bus_spider
from bustag.util import logger, APP_CONFIG

scheduler = None
loop = None


def download(loop, no_parse_links=False, urls=None):
    """
    下载更新数据

    Args:
        urls:tuple - tuple of urls
    """
    print('start download')
    # reset sys.argv
    sys.argv = sys.argv[:1]
    if not urls:
        logger.warning('no links to download')
        return
    count = APP_CONFIG['download.count']
    if no_parse_links:
        count = len(urls)
    extra_options = APP_CONFIG.get('options', {})
    options = {'no_parse_links': no_parse_links,
               'roots': urls, 'count': count}
    extra_options.update(options)

    aspider.download(loop, extra_options)
    try:
        import bustag.model.classifier as clf

        clf.recommend()
    except FileNotFoundError:
        print('还没有训练好的模型, 无法推荐')


def start_scheduler():
    global scheduler, loop

    interval = int(APP_CONFIG.get('download.interval', 1800))
    loop = asyncio.new_event_loop()
    scheduler = AsyncIOScheduler(event_loop=loop)
    t1 = datetime.now() + timedelta(seconds=1)
    int_trigger = IntervalTrigger(seconds=interval)
    date_trigger = DateTrigger(run_date=t1)
    urls = (APP_CONFIG['download.root_path'],)
    # add for down at server start
    scheduler.add_job(download, trigger=date_trigger, args=(loop, False, urls))
    scheduler.add_job(download, trigger=int_trigger, args=(loop, False, urls))
    scheduler.start()
    asyncio.set_event_loop(loop)
    loop.run_forever()


def add_download_job(urls):
    add_job(download, (urls,))


def add_job(job_func, args):
    '''
    add a job to scheduler
    '''
    default_args = (loop, True)
    default_args = default_args + args
    logger.debug(default_args)
    t1 = datetime.now() + timedelta(seconds=10)
    date_trigger = DateTrigger(run_date=t1)
    scheduler.add_job(job_func, trigger=date_trigger, args=default_args)
