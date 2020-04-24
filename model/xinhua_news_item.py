from mongoengine import DateTimeField
from mongoengine import Document
from mongoengine import StringField


class XinHuaNewsItem(Document):
    url = StringField(required=True)
    keyword = StringField(required=True)
    title = StringField(required=True)
    abstract = StringField()
    publish = DateTimeField()
    created = DateTimeField()

    def __str__(self):
        return f'<XinHuaNews url={self.url}, keyword={self.keyword}, title={self.title}, publish={self.publish}'
