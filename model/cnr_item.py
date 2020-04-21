from mongoengine import DateTimeField
from mongoengine import Document
from mongoengine import StringField


class CnrItem(Document):
    keyword = StringField(required=True)
    url = StringField()
    title = StringField()
    publish = DateTimeField()
    created = DateTimeField()

    def __str__(self):
        return f'<CNR keyword={self.keyword}, url={self.url}, title={self.title}, publish={self.publish}'
