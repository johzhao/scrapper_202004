from mongoengine import DateTimeField
from mongoengine import Document
from mongoengine import IntField
from mongoengine import StringField


class SinaWeibo(Document):
    keyword = StringField(required=True)
    url = StringField()
    title = StringField()
    username = StringField()
    publish = DateTimeField()
    content = StringField()
    forward_count = IntField()
    comment_count = IntField()
    favor_count = IntField()
    created = DateTimeField()

    def __str__(self):
        return (f'<SinaWeibo keyword={self.keyword}, url={self.url}, title={self.title}, '
                f'username={self.username}, publish={self.publish}, forward_count={self.forward_count} '
                f'comment_count={self.comment_count}, favor_count={self.favor_count}')
