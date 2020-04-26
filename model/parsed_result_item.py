from mongoengine import Document

__all__ = ['ParsedResultItem']


class ParsedResultItem(Document):
    meta = {
        'allow_inheritance': True,
    }

    @classmethod
    def store_item(cls, _: 'ParsedResultItem'):
        return NotImplemented

    def __str__(self):
        return NotImplemented
