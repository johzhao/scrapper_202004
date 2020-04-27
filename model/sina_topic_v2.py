import datetime

from mongoengine import IntField, DateTimeField, StringField
from model.parsed_result_item import ParsedResultItem


class WeiboTopicItem(ParsedResultItem):
    keyword = StringField(required=True)
    title = StringField(required=True, unique_with=['keyword'])
    url = StringField(required=True)

    @classmethod
    def store_item(cls, item: 'WeiboTopicItem'):
        cls.objects(keyword=item.keyword, title=item.title).update_one(url=item.url, upsert=True)

    def __str__(self):
        return f'<Weibo topic item keyword={self.keyword}, title={self.title}, url={self.url}>'


class WeiboTopicDetailItem(ParsedResultItem):
    keyword = StringField(required=True)
    title = StringField(required=True)
    date = DateTimeField(required=True, unique_with=['keyword', 'title'])
    read_count = IntField()
    discus_count = IntField()
    create_count = IntField()
    created = DateTimeField(required=True)

    @classmethod
    def store_item(cls, item: 'WeiboTopicDetailItem'):
        item.created = datetime.datetime.now()
        cls.objects(keyword=item.keyword, title=item.title, date=item.date).\
            update_one(read_count=item.read_count, discus_count=item.discus_count,
                       create_count=item.create_count, created=item.created, upsert=True)

    def __str__(self):
        return (f'<Weibo topic info item title={self.title}, keyword={self.keyword}, date={self.date}, '
                f'read={self.read_count}, discus={self.discus_count}, create={self.create_count}>')
