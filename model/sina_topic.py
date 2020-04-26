import datetime

from mongoengine import DateTimeField
from mongoengine import StringField

from model.parsed_result_item import ParsedResultItem


class SinaTopic(ParsedResultItem):
    keyword = StringField(required=True)
    topic = StringField(required=True)
    date = DateTimeField(required=True, unique_with=['_cls', 'keyword', 'topic'])
    url = StringField(required=True)
    read_count = StringField(required=True)
    comment_count = StringField(required=True)
    created = DateTimeField(required=True)

    @classmethod
    def store_item(cls, item: 'SinaTopic'):
        cls.objects(keyword=item.keyword, topic=item.topic, date=item.date)\
            .update_one(url=item.url, read_count=item.read_count, comment_count=item.comment_count,
                        created=datetime.datetime.now(), upsert=True)

    def __str__(self):
        return (f'<SinaTopic keyword={self.keyword}, topic={self.topic}, date={self.date}, url={self.url},'
                f' read_count={self.read_count}, comment_count={self.comment_count}')
