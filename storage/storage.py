import logging
from datetime import datetime

from mongoengine import Document
from mongoengine import connect

from model.sina_weibo import SinaWeibo

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Storage:

    def __init__(self, database: str, host: str, port: int):
        connect(database, host=host, port=port)

    def save_content(self, content: Document, type_: str):
        logger.info(f'Save type {type_}, content {content}')
        content.save()


def test_storage():
    import config
    storage = Storage(config.MONGO_DATABASE, config.MONGO_HOST, config.MONGO_PORT)

    item = SinaWeibo()
    item.keyword = 'keyword'
    item.url = 'https://s.weibo.com/weibo?q=%E7%96%AB%E6%83%85&xsort=hot&suball=1&timescope=custom:2020-01-01-0:2020-04-10-23&Refer=g&page=3'
    item.username = 'username'
    item.title = 'title'
    item.content = 'content'
    item.publish = datetime.now()
    item.forward_count = 100
    item.comment_count = 200
    item.favor_count = 300
    item.created = datetime.now()

    storage.save_content(item, 'detail')
