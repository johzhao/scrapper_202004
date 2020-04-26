import datetime

from mongoengine import Document, DateTimeField, StringField
from model.parsed_result_item import ParsedResultItem

__all__ = ['CnrItem', 'XinHuaNewsItem', 'PeopleItem', 'ChinaNewsItem', 'SinaNewsItem', 'GovItem', 'ChinaCdcItem',
           'ChinaItem', 'CctvItem']


class Task4BaseItem(ParsedResultItem):
    keyword = StringField(required=True)
    url = StringField(required=True, unique_with=['_cls', 'keyword'])
    title = StringField(required=True)
    abstract = StringField()
    publish = DateTimeField(required=True)
    created = DateTimeField(required=True)

    type_ = 'Base'

    @classmethod
    def store_item(cls, item: 'Task4BaseItem'):
        cls.objects(keyword=item.keyword, url=item.url)\
            .update_one(title=item.title, abstract=item.abstract, publish=item.publish,
                        created=datetime.datetime.now(), upsert=True)

    def __str__(self):
        return f'<{self.type_} item title={self.title}, keyword={self.keyword}, url={self.url}, publish={self.publish}>'


class CnrItem(Task4BaseItem):
    type_ = 'Cnr'


class XinHuaNewsItem(Task4BaseItem):
    type_ = 'Xinhua news'


class PeopleItem(Task4BaseItem):
    type_ = 'People'


class ChinaNewsItem(Task4BaseItem):
    type_ = 'China news'


class SinaNewsItem(Task4BaseItem):
    type_ = 'Sina news'


class GovItem(Task4BaseItem):
    type_ = 'Gov'


class ChinaCdcItem(Task4BaseItem):
    type_ = 'China cdc'


class ChinaItem(Task4BaseItem):
    type_ = 'China'


class CctvItem(Task4BaseItem):
    type_ = 'Cctv'
