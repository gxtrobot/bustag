from collections import defaultdict
import threading
import traceback
import sys
import os
import bottle
from multiprocessing import freeze_support
from bottle import route, run, template, static_file, request, response, redirect, hook

dirname = os.path.dirname(os.path.realpath(__file__))
if getattr(sys, 'frozen', False):
    dirname = sys._MEIPASS
print('dirname:' + dirname)
bottle.TEMPLATE_PATH.insert(0, dirname + '/views/')


@hook('before_request')
def _connect_db():
    dbconn.connect(reuse_if_open=True)


@hook('after_request')
def _close_db():
    if not dbconn.is_closed():
        dbconn.close()


@route('/static/<filepath:path>')
def send_static(filepath):
    return static_file(filepath, root=dirname+'/static/')


def _remove_extra_tags(item):
    limit = 10
    tags_dict = item.tags_dict
    tags = ['genre', 'star']
    for t in tags:
        tags_dict[t] = tags_dict[t][:limit]


@route('/')
def index():
    rate_type = RATE_TYPE.SYSTEM_RATE.value
    rate_value = int(request.query.get('like', RATE_VALUE.LIKE.value))
    page = int(request.query.get('page', 1))
    items, page_info = get_items(
        rate_type=rate_type, rate_value=rate_value, page=page)
    for item in items:
        _remove_extra_tags(item)
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
    for item in items:
        _remove_extra_tags(item)
    return template('tagit', items=items, page_info=page_info, like=rate_value, path=request.path)


@route('/tag/<fanhao>', method='POST')
def tag(fanhao):
    if request.POST.submit:
        formid = request.POST.formid
        item_rate = ItemRate.get_by_fanhao(fanhao)
        rate_value = request.POST.submit
        if not item_rate:
            rate_type = RATE_TYPE.USER_RATE
            ItemRate.saveit(rate_type, rate_value, fanhao)
            logger.debug(f'add new item_rate for fanhao:{fanhao}')
        else:
            item_rate.rate_value = rate_value
            item_rate.save()
            logger.debug(f'updated item_rate for fanhao:{fanhao}')
    page = int(request.query.get('page', 1))
    like = request.query.get('like')
    url = f'/tagit?page={page}&like={like}'
    if formid:
        url += f'#{formid}'
    redirect(url)


@route('/correct/<fanhao>', method='POST')
def correct(fanhao):
    if request.POST.submit:
        formid = request.POST.formid
        is_correct = int(request.POST.submit)
        item_rate = ItemRate.get_by_fanhao(fanhao)
        if item_rate:
            item_rate.rate_type = RATE_TYPE.USER_RATE
            if not is_correct:
                rate_value = item_rate.rate_value
                rate_value = 1 if rate_value == 0 else 0
                item_rate.rate_value = rate_value
            item_rate.save()
            logger.debug(
                f'updated item fanhao: {fanhao}, {"and correct the rate_value" if not is_correct else ""}')
    page = int(request.query.get('page', 1))
    like = int(request.query.get('like', 1))
    url = f'/?page={page}&like={like}'
    if formid:
        url += f'#{formid}'
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
    for local_item in items:
        LocalItem.loadit(local_item)
        _remove_extra_tags(local_item.item)
    return template('local', items=items, page_info=page_info, path=request.path)


@route('/local_play/<id:int>')
def local_play(id):
    local_item = LocalItem.update_play(id)
    file_path = local_item.path
    logger.debug(file_path)
    redirect(file_path)


@route('/load_db', method=['GET', 'POST'])
def load_db():
    msg = ''
    errmsg = ''
    if request.POST.submit:
        upload = request.files.get('dbfile')
        if upload:
            logger.debug(upload.filename)
            name = get_data_path('uploaded.db')
            upload.save(name, overwrite=True)
            logger.debug(f'uploaded file saved to {name}')
            try:
                tag_file_added, missed_fanhaos = load_tags_db()
            except DBError:
                errmsg = '数据库文件错误, 请检查文件是否正确上传'
            else:
                urls = [bus_spider.get_url_by_fanhao(
                        fanhao) for fanhao in missed_fanhaos]
                add_download_job(urls)
                msg = f'上传 {tag_file_added} 条用户打标数据, {len(missed_fanhaos)} 个番号, '
                msg += '  注意: 需要下载其他数据才能开始建模, 请等候一定时间'
        else:
            errmsg = '请上传数据库文件'
    return template('load_db', path=request.path, msg=msg, errmsg=errmsg)


@route('/about')
def about():
    return template('about', path=request.path)


app = bottle.default_app()


def start_app():
    t = threading.Thread(target=start_scheduler)
    t.start()
    run(host='0.0.0.0', server='paste', port=8000, debug=True)
    # run(host='0.0.0.0', port=8000, debug=True, reloader=False)


if __name__ == "__main__":
    try:
        freeze_support()
        from bustag import __version__
        print(f"Bustag server starting: version: {__version__}\n\n")
        import bustag.model.classifier as clf
        from bustag.util import logger, get_cwd, get_now_time, get_data_path
        from bustag.spider.db import (get_items, get_local_items, RATE_TYPE, RATE_VALUE, ItemRate,
                                      Item, LocalItem, DBError, db as dbconn)
        from bustag.spider import db
        from bustag.app.schedule import start_scheduler, add_download_job
        from bustag.spider import bus_spider
        from bustag.app.local import add_local_fanhao, load_tags_db
        start_app()
    except Exception as e:
        print('system error')
        traceback.print_exc()
    finally:
        print("Press Enter to continue ...")
        input()
        os._exit(1)
