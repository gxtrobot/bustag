from bottle import route, run, template, static_file
import bottle
import os
import sys
from bustag.spider.db import get_items
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


run(host='localhost', port=8080, debug=True, reloader=True)
