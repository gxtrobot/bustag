from collections import defaultdict
import threading
import sys
import os
import bottle
from multiprocessing import freeze_support
from bustag.util import logger, get_cwd, get_now_time
from bottle import route, run, template, static_file, request, response, redirect
from bustag.spider.db import get_items, get_local_items, RATE_TYPE, RATE_VALUE, ItemRate, Item, LocalItem
from bustag.spider import db
from bustag.app.schedule import start_scheduler, add_download_job
from bustag.spider import bus_spider
from bustag.app.local import add_local_fanhao

dirname = os.path.dirname(os.path.realpath(__file__))
if getattr(sys, 'frozen', False):
    dirname = sys._MEIPASS
print('dirname:' + dirname)
bottle.TEMPLATE_PATH.insert(0, dirname + '/views/')


@route('/static/<filepath:path>')
def send_static(filepath):
    return static_file(filepath, root=dirname+'/static/')


@route('/')
def index():
    rate_type = RATE_TYPE.SYSTEM_RATE.value
    rate_value = int(request.query.get('like', RATE_VALUE.LIKE.value))
    page = int(request.query.get('page', 1))
    items, page_info = get_items(
        rate_type=rate_type, rate_value=rate_value, page=page)

    today_update_count = db.get_today_update_count()
    today_recommend_count = db.get_today_recommend_count()
    msg = f'今日更新 {today_update_count} , 今日推荐 {today_recommend_count}'
    return template('index', items=items, page_info=page_info, like=rate_value, path=request.path, msg=msg)


@route('/tagit')
def tagit():
    rate_value = request.query.get('like', None)
    rate_value = None if rate_value == 'None' else rate_value
    rate_type = None
    if rate_value:
        rate_value = int(rate_value)
        rate_type = RATE_TYPE.USER_RATE
    page = int(request.query.get('page', 1))
    items, page_info = get_items(
        rate_type=rate_type, rate_value=rate_value, page=page)

    return template('tagit', items=items, page_info=page_info, like=rate_value, path=request.path)


@route('/tag/<id:int>', method='POST')
def tag(id):
    if request.POST.submit:
        formid = request.POST.formid
        item_rate = ItemRate.get_by_itemid(id)
        rate_value = request.POST.submit
        if not item_rate:
            rate_type = RATE_TYPE.USER_RATE
            item = Item.getit(id)
            ItemRate.saveit(rate_type, rate_value, item.fanhao)
            logger.debug(f'add new item_rate for id:{id}')
        else:
            item_rate.rate_value = rate_value
            item_rate.save()
            logger.debug(f'updated item_rate for id:{id}')
    page = int(request.query.get('page', 1))
    like = request.query.get('like')
    url = f'/tagit?page={page}&like={like}'
    if formid:
        url += f'#{formid}'
    print(url)
    redirect(url)


@route('/correct/<id:int>', method='POST')
def correct(id):
    if request.POST.submit:
        is_correct = int(request.POST.submit)
        item_rate = ItemRate.get_by_itemid(id)
        if item_rate:
            item_rate.rate_type = RATE_TYPE.USER_RATE
            if not is_correct:
                rate_value = item_rate.rate_value
                rate_value = 1 if rate_value == 0 else 0
                item_rate.rate_value = rate_value
            item_rate.save()
            logger.debug(
                f'updated item_id: {id}, {"and correct the rate_value" if not is_correct else ""}')
    page = int(request.query.get('page', 1))
    like = int(request.query.get('like', 1))
    url = f'/?page={page}&like={like}'
    print(url)
    redirect(url)


@route('/model')
def other_settings():
    try:
        _, model_scores = clf.load()
    except FileNotFoundError:
        model_scores = None
    return template('model', path=request.path, model_scores=model_scores)


@route('/do-training')
def do_training():
    error_msg = None
    model_scores = None
    try:
        _, model_scores = clf.train()
    except ValueError as ex:
        logger.exception(ex)
        error_msg = ' '.join(ex.args)
    return template('model', path=request.path, model_scores=model_scores, error_msg=error_msg)


@route('/local_fanhao', method=['GET', 'POST'])
def update_local_fanhao():
    msg = ''
    if request.POST.submit:
        fanhao_list = request.POST.fanhao
        tag_like = request.POST.tag_like == '1'
        missed_fanhao, local_file_count, tag_file_count = add_local_fanhao(
            fanhao_list, tag_like)
        if len(missed_fanhao) > 0:
            urls = [bus_spider.get_url_by_fanhao(
                fanhao) for fanhao in missed_fanhao]
            add_download_job(urls)
            msg = f'上传 {len(missed_fanhao)} 个番号, {local_file_count} 个本地文件'
            if tag_like:
                msg += f', {tag_file_count} 个打标为喜欢'
    return template('local_fanhao', path=request.path, msg=msg)


@route('/local')
def local():
    page = int(request.query.get('page', 1))
    items, page_info = get_local_items(page=page)
    for item in items:
        LocalItem.loadit(item)
    return template('local', items=items, page_info=page_info, path=request.path)


@route('/local_play/<id:int>')
def local_play(id):
    local_item = LocalItem.update_play(id)
    file_path = local_item.path
    print(file_path)
    redirect(file_path)


app = bottle.default_app()


def start_app():
    t = threading.Thread(target=start_scheduler)
    t.start()
    # run(host='0.0.0.0', server='paste', port=8000, debug=True)
    run(host='0.0.0.0', port=8000, debug=True, reloader=True)


if __name__ == "__main__":
    freeze_support()
    import bustag.model.classifier as clf
    start_app()
