'''
entry point for command line 
'''

import click
import sys
from aspider import aspider
from bustag.model.prepare import prepare_predict_data
from bustag.spider.db import Item, ItemRate, RATE_TYPE
import bustag.model.classifier as clf
from bustag.spider import bus_spider
from bustag.util import logger, APP_CONFIG


@click.command()
def recommend():
    '''
    根据现有模型预测推荐数据
    '''
    try:
        clf.recommend()
    except FileNotFoundError:
        click.echo('还没有训练好的模型, 无法推荐')


@click.command()
@click.option("--count", help="打印次数", type=int)
def download(count):
    """
    下载更新数据
    """
    sys.argv = sys.argv[:1]
    if count is not None:
        APP_CONFIG['download.count'] = count
    sys.argv.append(APP_CONFIG['download.root_path'])
    aspider.main()


@click.group()
def main():
    pass


main.add_command(download)
main.add_command(recommend)

if __name__ == "__main__":
    main()
