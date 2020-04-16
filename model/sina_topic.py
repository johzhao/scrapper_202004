from mongoengine import DateTimeField
from mongoengine import Document
from mongoengine import StringField


class SinaTopic(Document):
    keyword = StringField(required=True)
    topic = StringField(required=True)
    url = StringField(required=True)
    read_count = StringField(required=True)
    comment_count = StringField(required=True)
    created = DateTimeField(required=True)

    def __str__(self):
        return (f'<SinaTopic keyword={self.keyword}, url={self.url}, topic={self.topic}, read_count={self.read_count}, '
                f'comment_count={self.comment_count}')
