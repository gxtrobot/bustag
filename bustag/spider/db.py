'''
persist data to db
'''
from datetime import date
import datetime
import operator
from functools import reduce
import json
from peewee import *
from enum import IntEnum
from collections import defaultdict
from bustag.util import logger, get_data_path, to_localtime

DB_FILE = 'bus.db'
db = SqliteDatabase(get_data_path(DB_FILE))


class BaseModel(Model):
    class Meta:
        database = db
        legacy_table_names = False


class ExistError(Exception):
    pass


class Item(BaseModel):
    '''
    item table
    '''
    title = CharField()
    fanhao = CharField()
    url = CharField(unique=True)
    release_date = DateField()
    add_date = DateTimeField(default=datetime.datetime.now)
    meta_info = TextField()

    def __repr__(self):
        return f'<Item:{self.id} {self.title}>'

    @staticmethod
    def saveit(meta_info):
        item_release_date = date.fromisoformat(meta_info.pop('release_date'))
        item_fanhao = meta_info.pop('fanhao')
        item_title = meta_info.pop('title')
        item_url = meta_info.pop('url')
        item_meta = json.dumps(meta_info)
        try:
            item = Item.create(fanhao=item_fanhao, title=item_title, url=item_url,
                               release_date=item_release_date, meta_info=item_meta)
            logger.debug(f'save item:  {item}')
        except IntegrityError as ex:
            raise ExistError()
        return item

    @staticmethod
    def loadit(item):
        meta = json.loads(item.meta_info)
        item.cover_img_url = meta['cover_img_url']
        tags = []
        series = item.fanhao.split('-')[0]
        for t in item.tags_list:
            tags.append(t.tag.value)
        tags.append(series)
        tags = set(tags)
        item.tags = tags
        item.add_date = to_localtime(item.add_date)

    @staticmethod
    def getit(id):
        item = Item.get_by_id(id)
        return item

    @staticmethod
    def get_tags_dict(item):
        tags = item.tags_list
        tags_dict = defaultdict(list)
        for t in item.tags_list:
            if t.tag.type_ in ['genre', 'star']:
                tags_dict[t.tag.type_].append(t.tag.value)
        item.tags_dict = tags_dict


class Tag(BaseModel):
    '''
    tag table
    '''
    type_ = CharField(column_name='type')
    value = CharField(unique=True)
    url = CharField()

    def __repr__(self):
        return f'<Tag {self.value}>'

    @staticmethod
    def saveit(tag_info):
        try:
            tag = Tag.create(type_=tag_info.type, value=tag_info.value,
                             url=tag_info.link)
            logger.debug(f'save tag:  {tag}')
        except IntegrityError as ex:
            tag = Tag.get(Tag.value == tag_info.value)

        return tag


class ItemTag(BaseModel):
    item = ForeignKeyField(Item, backref='tags_list')
    tag = ForeignKeyField(Tag, backref='items')

    @staticmethod
    def saveit(item, tag):
        try:
            item_tag = ItemTag.create(item=item, tag=tag)
            logger.debug(f'save tag_item: {item_tag}')
        except Exception as ex:
            logger.exception(ex)

        return item_tag

    def __repr__(self):
        return f'<ItemTag {self.item.title} - {self.tag.value}>'


class RATE_TYPE(IntEnum):
    NOT_RATE = 0
    USER_RATE = 1
    SYSTEM_RATE = 2


class RATE_VALUE(IntEnum):
    LIKE = 1
    DISLIKE = 0


class ItemRate(BaseModel):
    rate_type = IntegerField()
    rate_value = IntegerField()
    item = ForeignKeyField(Item, backref='rated_items', unique=True)
    rete_time = DateTimeField(default=datetime.datetime.now)

    @staticmethod
    def saveit(rate_type, rate_value, item):
        try:
            item_rate = ItemRate.create(
                item=item, rate_type=rate_type, rate_value=rate_value)
            logger.debug(f'save ItemRate: {item_rate}')
        except Exception as ex:
            logger.exception(ex)

        return item_rate

    @staticmethod
    def get_by_itemid(item_id):
        item_rates = ItemRate.select().where(ItemRate.item_id == item_id).limit(1)
        return item_rates[0] if len(item_rates) > 0 else None


def save(meta_info, tags):
    item_title = meta_info['title']
    try:
        item = Item.saveit(meta_info)
    except ExistError:
        logger.debug(f'item exists: {item_title}')
    else:
        for tag_info in tags:
            tag = Tag.saveit(tag_info)
            ItemTag.saveit(item, tag)


def test_save():
    item_url = 'https://www.cdnbus.bid/MADM-116'
    item_title = 'test item'
    item_release_date = date(2019, 7, 19)
    item_meta_info = ''
    item = Item(title=item_title, url=item_url,
                release_date=item_release_date, meta_info=item_meta_info)
    item.save()

    tag1 = Tag.create(type_='genre', value='素人',
                      url='https://www.cdnbus.bid/genre/s1')
    tag2 = Tag.create(type_='star', value='樱田',
                      url='https://www.cdnbus.bid/star/dbd')
    tag3 = Tag.create(type_='genre', value='高清',
                      url='https://www.cdnbus.bid/genre/x1')
    ItemTag.create(item=item, tag=tag1)
    ItemTag.create(item=item, tag=tag2)


def get_items(rate_type=None, rate_value=None, page=1, page_size=10):
    '''
    get required items based on some conditions
    '''
    items = []
    clauses = []
    if rate_type is not None:
        clauses.append(ItemRate.rate_type == rate_type)
    else:
        clauses.append(ItemRate.rate_type.is_null())
    if rate_value is not None:
        clauses.append(ItemRate.rate_value == rate_value)
    q = (Item.select(Item, ItemRate)
         .join(ItemRate, JOIN.LEFT_OUTER, attr='item_rate')
         .where(reduce(operator.and_, clauses))
         .order_by(ItemRate.id.desc())
         )
    total_items = q.count()
    if not page is None:
        q = q.paginate(page, page_size)
    for item in q:
        Item.loadit(item)
        if hasattr(item, 'item_rate'):
            item.rate_value = item.item_rate.rate_value
        else:
            item.rate_value = None
        items.append(item)

    total_pages = (total_items + page_size - 1) // page_size
    page_info = (total_items, total_pages, page, page_size)
    return items, page_info


def init():
    db.connect()
    db.create_tables([Item, Tag, ItemTag, ItemRate])


init()
