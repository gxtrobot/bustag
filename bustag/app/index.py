from bottle import route, run, template, static_file, request, response, redirect
import bottle
import os
import sys
from bustag.spider.db import get_items, RATE_TYPE, ItemRate, Item
dirname = os.path.dirname(sys.argv[0])

print(dirname)
bottle.TEMPLATE_PATH.insert(0, dirname+'/views/')


@route('/static/<filepath:path>')
def send_static(filepath):
    return static_file(filepath, root=dirname+'/static/')


@route('/')
def index():
    items, page_info = get_items(page=1)
    print(items[0])
    print(bottle.TEMPLATE_PATH)
    return template('index', items=items)


@route('/tagit')
def tagit():
    page = int(request.query.get('page', 1))
    print(page)
    items, page_info = get_items(page=page)
    return template('tagit', items=items, page_info=page_info)


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
