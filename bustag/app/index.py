from bottle import route, run, template, static_file, request, response, redirect
import bottle
import os
import sys
from bustag.spider.db import get_items, RATE_TYPE, RATE_VALUE, ItemRate, Item
dirname = os.path.dirname(sys.argv[0])

print(dirname)
bottle.TEMPLATE_PATH.insert(0, dirname+'/views/')


@route('/static/<filepath:path>')
def send_static(filepath):
    return static_file(filepath, root=dirname+'/static/')


@route('/')
def index():
    rate_type = RATE_TYPE.SYSTEM_RATE.value
    rate_value = int(request.query.get('like', RATE_VALUE.LIKE.value))
    print(rate_value)
    page = int(request.query.get('page', 1))
    items, page_info = get_items(
        rate_type=rate_type, rate_value=rate_value, page=page)
    print(bottle.TEMPLATE_PATH)
    return template('index', items=items, page_info=page_info, like=rate_value)


@route('/tagit')
def tagit():
    rate_value = request.query.get('like', None)
    rate_type = None
    if rate_value:
        rate_value = int(rate_value)
        rate_type = RATE_TYPE.USER_RATE
    page = int(request.query.get('page', 1))
    items, page_info = get_items(
        rate_type=rate_type, rate_value=rate_value, page=page)
    return template('tagit', items=items, page_info=page_info, like=rate_value)


@route('/tag/<id:int>', method='POST')
def tag(id):
    if request.POST.submit:
        rate_type = RATE_TYPE.USER_RATE
        rate_value = request.POST.submit
        item = Item.getit(id)
        ItemRate.saveit(rate_type, rate_value, item)
    page = int(request.query.get('page', 1))
    url = f'/tagit?page={page}'
    print(url)
    redirect(url)


run(host='0.0.0.0', port=8080, debug=True, reloader=True)
