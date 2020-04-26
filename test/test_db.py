from mongoengine import Document
from mongoengine import StringField
from mongoengine import connect

import config


class BaseItem(Document):
    title = StringField(required=True)
    url = StringField(required=True)
    keyword = StringField(required=True, unique_with=['_cls', 'url'])
    meta = {'allow_inheritance': True}

    type_ = 'Base'

    @classmethod
    def store_item(cls, item: 'BaseItem'):
        cls.objects(url=item.url, keyword=item.keyword).update_one(title=item.title, upsert=True)

    def __str__(self):
        return f'<{self.type_} item title={self.title}, keyword={self.keyword}, url={self.url}>'


class TestItem1(BaseItem):

    type_ = 'Test1'


class TestItem2(BaseItem):

    type_ = 'Test2'


def test_db():
    connect('test_db', host=config.MONGO_HOST, port=config.MONGO_PORT)

    item1 = TestItem1()
    item1.url = 'url'
    item1.keyword = 'keyword'
    item1.title = 'title1'
    item1.__class__.store_item(item1)
    print(item1)

    item2 = TestItem2()
    item2.url = 'url'
    item2.keyword = 'keyword'
    item2.title = 'title2'
    item2.__class__.store_item(item2)
    print(item2)
