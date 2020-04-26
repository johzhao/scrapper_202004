from mongoengine import DateTimeField
from mongoengine import Document
from mongoengine import IntField
from mongoengine import StringField

from model.parsed_result_item import ParsedResultItem


class SinaWeibo(ParsedResultItem):
    keyword = StringField(required=True)
    url = StringField(required=True)
    title = StringField(required=True)
    username = StringField(required=True)
    publish = DateTimeField(required=True)
    content = StringField()
    forward_count = IntField()
    comment_count = IntField()
    favor_count = IntField()
    created = DateTimeField()

#     @classmethod
#     def store_item(cls, item: 'ParsedResultItem'):
#         cls.objects(keyword=item.keyword, topic=item.topic, date=item.date)\
#             .update_one(url=item.url, read_count=item.read_count, comment_count=item.comment_count,
#                         created=datetime.datetime.now(), upsert=True)
#
#     def __str__(self):
#         return (f'<SinaWeibo keyword={self.keyword}, url={self.url}, title={self.title}, '
#                 f'username={self.username}, publish={self.publish}, forward_count={self.forward_count} '
#                 f'comment_count={self.comment_count}, favor_count={self.favor_count}')
